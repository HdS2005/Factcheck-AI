# FactCheck AI

> Built as part of the CogCulture Product Management Assessment

## The Problem

Marketing, research, and business documents often contain outdated statistics, hallucinated figures, or unverified claims. Manually fact-checking them is time-consuming, inconsistent, and prone to oversight.

## The Solution

**FactCheck AI** acts as a "Truth Layer" for documents. Users can upload any PDF, and the system automatically extracts factual claims, cross-references them against live web sources, and highlights potentially inaccurate information before it reaches stakeholders or audiences.

---

## How It Works

1. **Upload** – Upload any PDF document.
2. **Extract** – AI identifies specific, verifiable claims such as statistics, dates, financial figures, scientific facts, and named events.
3. **Search** – Each claim is cross-referenced against live web results using Serper API.
4. **Verify** – Claims are classified into one of three categories:

   * ✅ **Verified** – Matches current web evidence.
   * ⚠️ **Inaccurate** – Conflicts with available evidence.
   * ❓ **Unverifiable** – Insufficient evidence found.
5. **Report** – Users receive a structured verification report with explanations for every claim.

---

## Key Features

* PDF-based fact checking
* Automated claim extraction
* Live web verification
* Detailed verification logs
* Modern, user-friendly interface
* Parallel claim processing for faster analysis

---

## Tech Stack

| Layer       | Technology                     |
| ----------- | ------------------------------ |
| Frontend    | Streamlit                      |
| AI Model    | Groq (Llama 3.3 70B Versatile) |
| Web Search  | Serper API                     |
| PDF Parsing | pdfplumber                     |
| Deployment  | Streamlit Cloud                |
| Concurrency | ThreadPoolExecutor             |

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/factcheck-ai.git
cd factcheck-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` and add:

```toml
GROQ_API_KEY = "your_groq_api_key"
SERPER_API_KEY = "your_serper_api_key"
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Improvements

* Batch verification to further reduce response time
* Source citations for every verdict
* Exportable PDF verification reports
* Support for DOCX and PPT uploads
* Confidence scoring for each claim

---

## Assessment Context

This project was developed as part of the **CogCulture Product Management Trainee Assessment** to demonstrate problem-solving ability, product thinking, technical execution, and rapid prototyping.

The objective was to design a solution that addresses a real-world pain point using AI while maintaining a simple and intuitive user experience.
