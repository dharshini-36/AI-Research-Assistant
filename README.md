# 🤖 AI Research Assistant Agent

An autonomous, agentic AI application built with **Streamlit** that researches any topic end-to-end: it plans the research, searches the web, summarizes findings, generates study notes and interview questions, builds an interactive quiz, and exports everything as a PDF report.

---

## ✨ Features

- **🧠 Research Planner Agent** – breaks a topic down into key concepts, questions, and keywords before researching.
- **🔎 Web Research Agent** – runs multiple DuckDuckGo searches (definition, applications, advantages/challenges) and collects real sources.
- **📝 Summary Agent** – turns collected results into a structured, student-friendly summary (Introduction → Future Scope).
- **📚 Study Notes Agent** – generates in-depth notes suitable for study and technical interviews.
- **💼 Interview Question Agent** – produces 15 basic/intermediate/advanced Q&A pairs.
- **❓ Interactive Quiz Agent** – generates a 5-question multiple-choice quiz. Questions are parsed into real, clickable options — you answer first, then submit to see your score, the correct answers, and explanations (no more answers being spoiled up front).
- **📄 PDF Report Export** – bundles the plan, summary, notes, interview questions, and quiz into a single downloadable PDF, with markdown (`**bold**`, `## headings`) properly rendered instead of showing raw `**`/`#` symbols.
- **📚 Research History** – sidebar keeps track of topics researched during the session.

---

## 🗂 Workflow

```
User Topic → AI Planner → Web Research → Summary → Notes/Interview Qs → Quiz → PDF Report
```

---

## 🛠 Tech Stack

| Purpose            | Library              |
|---------------------|-----------------------|
| App / UI            | [Streamlit](https://streamlit.io) |
| AI reasoning        | [Groq API](https://groq.com) (`llama-3.3-70b-versatile`) |
| Web search           | [duckduckgo-search](https://pypi.org/project/duckduckgo-search/) |
| PDF generation       | [ReportLab](https://www.reportlab.com/) |

---

## 📦 Requirements

Create a `requirements.txt` with:

```
streamlit
groq
reportlab
duckduckgo-search
```

Install them:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

The app needs a **Groq API key**. You can supply it either via:

**Option A — Streamlit secrets** (recommended for deployment)

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Option B — Environment variable**

```bash
export GROQ_API_KEY="your_groq_api_key_here"   # macOS/Linux
setx GROQ_API_KEY "your_groq_api_key_here"      # Windows
```

If no key is found, the app still runs, but AI-powered sections will show:
`⚠️ Groq API key not configured.`

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

---

## 🧭 Using the App

1. **🏠 Home** – overview of the workflow.
2. **🔍 Research** – enter a topic and click **Start Research**. The agent plans, extracts keywords, searches the web, and writes a summary.
3. **📝 Notes** – auto-generates detailed study notes and interview questions from the research summary.
4. **❓ Quiz** – answer each multiple-choice question, then click **Submit Quiz** to see your score, correct answers, and explanations. Use **Retake Quiz** to try again.
5. **📄 Download PDF** – exports the full report (plan, summary, notes, interview Q&A, quiz) as a formatted PDF.
6. **About** – project and tech-stack details.

> Research history for the current session is listed in the sidebar.

---

## 📁 Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚠️ Notes & Limitations

- Web search results depend on DuckDuckGo availability and may occasionally be rate-limited.
- Quiz parsing expects the AI to follow the `Question / A) / B) / C) / D) / Correct Answer / Explanation` format; if the model deviates, the app falls back to showing the raw AI text.
- All data is stored in Streamlit's session state, so it resets when the app restarts or the browser session ends.

---

# 👩‍💻 Author

**Dharshini N**

B.Sc Computer Science with Artificial Intelligence

---

# 📜 License

This project is created for educational and portfolio purposes.
