# FactCheck AI

> Built as part of the CogCulture Product Management Assessment

## The Problem
Marketing and research documents frequently contain outdated statistics, hallucinated figures, or unverified claims. Manually fact-checking these is slow, inconsistent, and often skipped entirely.

## The Solution
Veridox is a web app that acts as a "Truth Layer" — upload any PDF and it automatically extracts every factual claim, cross-references it against live web data, and flags what's wrong before it reaches your audience.

## Live App
**[Try it here →](https://your-app-url.streamlit.app)**

## How It Works
1. **Upload** — User uploads any PDF document
2. **Extract** — Gemini AI reads the document and identifies all specific, verifiable claims (stats, dates, figures, named events)
3. **Verify** — Each claim is searched on the live web via Serper API
4. **Report** — Every claim is flagged as:
   - Verified — matches live web data
   - Inaccurate — figure is outdated or wrong (correct figure shown)
   - Unverifiable — no supporting evidence found

## Tech Stack
| Layer | Tool |
|-------|------|
| Frontend | Streamlit |
| AI Model | Google Gemini 2.0 Flash |
| Web Search | Serper API |
| PDF Parsing | pdfplumber |
| Deployment | Streamlit Cloud |

## Running Locally

```bash
git clone https://github.com/YOUR_USERNAME/veridox.git
cd veridox
pip install -r requirements.txt
```

Add your API keys in `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_key_here"
SERPER_API_KEY = "your_key_here"
```

Then run:
```bash
streamlit run app.py
```

---

*Submission for CogCulture PM Trainee Assessment — Part 2*