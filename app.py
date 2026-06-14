import streamlit as st
import pdfplumber
from groq import Groq
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. Page Configuration
st.set_page_config(page_title="FactCheck AI", page_icon="✓", layout="wide")

# 2. Hardcore Override - Complete Global Text Visibility Patches
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base Reset */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #fbfbfc !important;
    color: #111111 !important;
}

/* Hide Default Clutter */
[data-testid="stHeader"], [data-testid="stToolbar"], footer {
    display: none !important;
}

/* Fixed Top Bar */
.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 40px;
    background: rgba(251, 251, 252, 0.9);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid #edf0f2;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 999;
}
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 700;
    font-size: 18px;
    letter-spacing: -0.03em;
    color: #111111;
}
.brand-icon {
    background: #111111;
    color: #ffffff;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 14px;
}
.app-status-pill {
    font-size: 12px;
    font-weight: 500;
    background: #eef2f6;
    color: #475569;
    padding: 4px 12px;
    border-radius: 100px;
    border: 1px solid #e2e8f0;
}

/* Hard Adjusted Title Spacing */
.hero-box {
    text-align: center;
    max-width: 640px;
    margin: 110px auto 20px auto;
    padding: 0;
}
.hero-title {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -0.04em;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.1 !important;
    color: #111111;
}
.hero-title em { 
    font-weight: 300; 
    color: #64748b; 
    font-style: italic;
}
.hero-subtitle {
    font-size: 15px;
    color: #475569;
    line-height: 1.4;
    margin: 8px 0 0 0 !important;
}

/* NATIVE STREAMLIT FILE UPLOADER CARD OVERRIDE */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 24px !important;
    box-shadow: 0 4px 25px rgba(0,0,0,0.015) !important;
    margin-top: 10px !important;
}

/* Main Outer Label Text Fix (Upload Verification Target Label) */
[data-testid="stFileUploader"] > label {
    color: #111111 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    margin-bottom: 12px !important;
}

/* Dropzone Inside Container Fix */
[data-testid="stFileUploaderDropzone"] {
    background: #f8fafc !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 24px !important;
}

/* CRITICAL TEXT VISIBILITY PATCH: Forces missing native help text/file limits to show clearly */
[data-testid="stFileUploaderDropzone"] p, 
[data-testid="stFileUploaderDropzone"] span, 
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stUploadDropzoneInstructions"] small,
.st-emotion-cache-1ae2hue, 
.st-emotion-cache-j7qwjs {
    color: #475569 !important; /* High contrast slate color for instructions */
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* CRISP WHITE TEXT FIX FOR UPLOADED FILE BLOCKS */
[data-testid="stFileUploaderFileData"] {
    background-color: #111111 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploaderFileData"] div,
[data-testid="stFileUploaderFileData"] span,
[data-testid="stFileUploaderFileData"] p {
    color: #ffffff !important;  
    font-weight: 500 !important;
}
[data-testid="stFileUploaderFileData"] svg {
    fill: #ffffff !important; 
}

/* Native widget secondary action elements (+) text override */
[data-testid="stFileUploaderDropzone"] button {
    background: #111111 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 8px 16px !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: #1f2937 !important;
    color: #ffffff !important;
}
[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}

/* MAIN RUN BUTTON FIXED */
.stButton>button {
    background: #111111 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.15s ease-in-out;
    margin-top: 10px;
}
.stButton>button:hover {
    background: #1f2937 !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Output Metric Blocks */
.custom-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 4px 30px rgba(0,0,0,0.015);
    margin-top: 24px;
}
.card-title-main {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: -0.01em;
    margin-bottom: 6px;
    color: #111111;
}
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.m-val { font-size: 32px; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }
.m-lbl { font-size: 12px; font-weight: 600; color: #64748b; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
.txt-verified { color: #10b981; }
.txt-inaccurate { color: #f59e0b; }
.txt-unverifiable { color: #ef4444; }

/* Logs Rows */
.report-row {
    padding: 18px 0;
    border-bottom: 1px solid #f1f5f9;
}
.report-row:last-child { border-bottom: none; }
.tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 5px;
    letter-spacing: 0.05em;
    margin-right: 12px;
}
.tag-verified { background: #dcfce7; color: #15803d; }
.tag-inaccurate { background: #fef3c7; color: #b45309; }
.tag-unverifiable { background: #fee2e2; color: #b91c1c; }

.claim-text { font-size: 14.5px; font-weight: 600; color: #111111; display: inline; vertical-align: middle; }
.expl-text { font-size: 13.5px; color: #475569; margin-top: 8px; line-height: 1.5; }

.footer {
    text-align: center;
    padding: 30px 0;
    font-size: 12px;
    color: #94a3b8;
    border-top: 1px solid #e2e8f0;
    margin-top: 80px;
}
</style>

<div class="nav-bar">
    <div class="brand"><span class="brand-icon">✓</span> FactCheck AI</div>
    <div class="app-status-pill">Engine Active</div>
</div>

<div class="hero-box">
    <div class="hero-title">Every claim. <em>Verified.</em></div>
    <div class="hero-subtitle">Upload any document to scan factual assertions and cross-reference them live against web sources.</div>
</div>
""", unsafe_allow_html=True)


# 3. Keys Check
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", os.getenv("SERPER_API_KEY", ""))

if not GROQ_API_KEY or not SERPER_API_KEY:
    st.error("Infrastructure Configuration Error: Verify execution API tokens.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# 4. Core Logic Functions
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    return text.strip()

def extract_claims(text):
    prompt = f"""
You are a fact-checking assistant.

Extract all specific, verifiable claims from this document.

Focus on:
- statistics
- percentages
- dates
- financial figures
- scientific facts
- named events
- technical data

Ignore opinions.

Return ONLY a valid JSON array.

Example:
[
    "Claim 1",
    "Claim 2"
]

Document:
{text[:6000]}
"""

    raw = ask_groq(prompt)

    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)

def search_web(query):
    try:
        res = requests.post("https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": 5}, timeout=10).json()
        return "\n".join(f"{r.get('title','')}: {r.get('snippet','')}" for r in res.get("organic",[]))
    except Exception:
        return ""

def verify_claim(claim, snippets):
    prompt = f"""
Fact-check this claim using the web results below.

Claim:
"{claim}"

Web Results:
{snippets}

Return ONLY valid JSON.

Example:
{{
    "verdict": "Verified",
    "explanation": "one sentence"
}}

Possible verdicts:
- Verified
- Inaccurate
- Unverifiable
"""

    raw = ask_groq(prompt)

    raw = raw.replace("```json", "").replace("```", "").strip()

    return json.loads(raw)


# 5. Native Centered Component Container Grid
_, center_col, _ = st.columns([1, 2.2, 1])

with center_col:
    # Direct File Uploader Injection (Saves layout gaps entirely)
    uploaded_file = st.file_uploader("Upload Verification Target", type=["pdf"], label_visibility="visible")

    if uploaded_file:
        with st.spinner("Analyzing text schema arrays..."):
            text = extract_text(uploaded_file)
        
        if not text:
            st.error("Processing Fault: Text extraction matrix empty.")
            st.stop()
            
        st.success(f"Staged file successfully: {uploaded_file.name}")

        if st.button("Run Diagnostics Engine"):
            with st.spinner("Extracting claim instances..."):
                try:
                    claims = extract_claims(text)
                except Exception as e:
                    st.error(f"Execution Error: {e}")
                    st.stop()

            if not claims:
                st.info("No explicit fact elements found within document text stream.")
                st.stop()

            # Sequential thread run loop
            results = []
            progress = st.progress(0)

            def process_claim(claim):
                try:
                    snippets = search_web(claim)
                    vdata = verify_claim(claim, snippets)

                    return {
                        "claim": claim,
                        "verdict": vdata.get("verdict", "Unverifiable"),
                        "explanation": vdata.get("explanation", "")
                    }

                except Exception:
                    return {
                        "claim": claim,
                        "verdict": "Unverifiable",
                        "explanation": "System runtime checking timeout."
                    }

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(process_claim, claim)
                    for claim in claims
                ]

                completed = 0

                for future in as_completed(futures):
                    results.append(future.result())

                    completed += 1
                    progress.progress(completed / len(claims))

            v_count = sum(1 for r in results if r["verdict"] == "Verified")
            i_count = sum(1 for r in results if r["verdict"] == "Inaccurate")
            u_count = sum(1 for r in results if r["verdict"] == "Unverifiable")

            # Metrics Card Panel Output
            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card"><div class="m-val txt-verified">{v_count}</div><div class="m-lbl">Verified</div></div>
                <div class="metric-card"><div class="m-val txt-inaccurate">{i_count}</div><div class="m-lbl">Inaccurate</div></div>
                <div class="metric-card"><div class="m-val txt-unverifiable">{u_count}</div><div class="m-lbl">Unverifiable</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Deep analytical trace matrix
            st.markdown("""
            <div class="custom-card">
                <div class="card-title-main" style="border-bottom: 1px solid #e2e8f0; padding-bottom:12px; margin-bottom:14px;">
                    Verification Engine Logs
                </div>
            """, unsafe_allow_html=True)

            for r in results:
                tag_class = "tag-unverifiable"
                if r["verdict"] == "Verified": tag_class = "tag-verified"
                elif r["verdict"] == "Inaccurate": tag_class = "tag-inaccurate"

                st.markdown(f"""
                <div class="report-row">
                    <div>
                        <span class="tag {tag_class}">{r['verdict']}</span>
                        <div class="claim-text">{r['claim']}</div>
                    </div>
                    <div class="expl-text">{r['explanation']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

# Footer Global Block
st.markdown("""
<div class="footer">
    FactCheck AI &bull; Automated Realtime Validation Systems
</div>
""", unsafe_allow_html=True)
