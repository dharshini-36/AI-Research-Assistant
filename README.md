# 🤖 AI Research Assistant Agent

An autonomous, multi-agent AI application built with **Streamlit** that researches any topic end-to-end: it plans the work, retrieves or searches for information, critiques and improves its own summary, remembers what it's learned, and generates study notes, an interactive quiz, and a downloadable PDF report.

---

## ✨ Features

- **🤖 Manager Agent** – decides the execution plan for the topic before any other agent runs (shown to the user for transparency).
- **🧠 Research Planner Agent** – breaks the topic into key concepts, questions, and keywords.
- **🔑 Keyword Extraction Agent** – pulls out searchable keywords.
- **📚 Retrieval + Web Research Agent (RAG)** – first checks the **Pinecone** vector knowledge base for existing knowledge on the topic; only falls back to live DuckDuckGo search if nothing relevant is stored yet, then embeds and stores what it finds for next time.
- **📝 Summary Agent** – combines retrieved knowledge + fresh web results into a structured, deduplicated, student-friendly summary.
- **🔍 Critic Agent** – reviews the summary for completeness (definition, concepts, applications, advantages, challenges, future scope); if something's missing, triggers another research + summary pass automatically.
- **🧵 Memory Agent** – stores the topic, keywords, and final summary back into Pinecone so future research on related topics can reuse it.
- **📚 Study Notes Agent** – generates in-depth notes suitable for study and technical interviews.
- **💼 Interview Question Agent** – produces 15 basic/intermediate/advanced Q&A pairs.
- **❓ Interactive Quiz Agent** – generates a 5-question multiple-choice quiz, parsed into real clickable options. Answer first, then submit to see your score, correct answers, and explanations.
- **📄 PDF Report Export** – bundles the manager's plan, research plan, summary, notes, interview questions, and quiz into one downloadable PDF, with markdown (`**bold**`, `## headings`) rendered properly instead of showing raw symbols.
- **📚 Research History** – sidebar tracks topics researched during the session.

---

## 🗂 Agent Workflow

```
User Topic
   → Manager Agent (plans execution)
   → Planner Agent
   → Keyword Agent
   → Retrieval / Web Research Agent (Pinecone RAG + DuckDuckGo)
   → Summary Agent
   → Critic Agent (loops back to research if gaps found)
   → Memory Agent (stores to Pinecone)
   → Notes / Interview Question Agent
   → Quiz Agent
   → PDF Report
```

---

## 🛠 Tech Stack

| Purpose              | Library |
|-----------------------|---------|
| App / UI              | [Streamlit](https://streamlit.io) |
| AI reasoning          | [Groq API](https://groq.com) (`llama-3.3-70b-versatile`) |
| Vector memory / RAG   | [Pinecone](https://www.pinecone.io/) |
| Embeddings            | [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) |
| Text chunking         | [langchain-text-splitters](https://pypi.org/project/langchain-text-splitters/) |
| Web search            | [duckduckgo-search](https://pypi.org/project/duckduckgo-search/) |
| PDF generation        | [ReportLab](https://www.reportlab.com/) |
| PDF reading (uploads) | [pypdf](https://pypi.org/project/pypdf/) |

---

## 📦 Requirements

`requirements.txt`:

```
streamlit
groq
duckduckgo-search
reportlab
pinecone
sentence-transformers
langchain-text-splitters
pypdf
```

Install:

```bash
pip install -r requirements.txt
```

> Only the packages actually imported by `app.py` are listed. Avoid adding the full `langchain` / `langchain-community` / `langchain-pinecone` packages unless you actually use them — they pull in a very large, fast-moving dependency tree and can cause `pip`'s resolver to hang/backtrack for a long time, especially unpinned.

---

## 🔑 Configuration

The app needs two API keys.

**Option A — Streamlit secrets** (recommended for deployment)

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
PINECONE_API_KEY = "your_pinecone_api_key_here"
```

**Option B — Environment variables**

```bash
export GROQ_API_KEY="your_groq_api_key_here"
export PINECONE_API_KEY="your_pinecone_api_key_here"
```

**Pinecone setup:** the app expects an existing index named **`research-agent`** with a dimension matching `all-MiniLM-L6-v2` (**384**), metric `cosine`. Create it once in the Pinecone console (or via the Pinecone API) before running the app — the code does not create the index automatically.

If `GROQ_API_KEY` is missing, AI-powered sections show `⚠️ Groq API key not configured.`
If `PINECONE_API_KEY` is missing, the app still runs — it just skips memory/RAG (`index = None`) and always falls back to live web search.

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

---

## 🧭 Using the App

1. **🏠 Home** – overview of the agent workflow.
2. **🔍 Research** – enter a topic and click **Start Research**. Watch each agent run in sequence: Manager → Planner → Keywords → Retrieval/Search → Summary → Critic (which may trigger a second research pass) → Memory.
3. **📝 Notes** – auto-generates detailed study notes and interview questions from the summary.
4. **❓ Quiz** – answer each multiple-choice question, then click **Submit Quiz** to see your score, correct answers, and explanations. **Retake Quiz** to try again.
5. **📄 Download PDF** – exports the full report (manager plan, research plan, summary, notes, interview Q&A, quiz) as a formatted PDF.
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

- The **Manager Agent's plan is currently advisory** — it's generated and displayed for transparency, but the other agents always run in the same fixed order regardless of what the plan says. Making execution actually branch on the plan is a natural next step.
- **Critic Agent loop is capped at one retry** — if the second summary pass is still judged incomplete, the app does not loop again.
- Web search results depend on DuckDuckGo availability and may occasionally be rate-limited.
- Quiz parsing expects the AI to follow the `Question / A) / B) / C) / D) / Correct Answer / Explanation` format; if the model deviates, the app falls back to showing the raw AI text.
- Session-level data (`research_data`, quiz progress, history) resets when the app restarts or the browser session ends. Long-term memory only persists at the **Pinecone** layer (embeddings of topics/summaries), not full UI state.

---

# 👩‍💻 Author

**Dharshini N**

B.Sc Computer Science with Artificial Intelligence

---

# 📜 License

This project is created for educational and portfolio purposes.
