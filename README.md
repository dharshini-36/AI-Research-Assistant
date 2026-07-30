# 🤖 AI Research Assistant Agent using RAG & Pinecone

An intelligent **Agentic AI Research Assistant** built with **Streamlit**, **Groq LLM**, **Pinecone Vector Database**, and **Retrieval-Augmented Generation (RAG)**. The application autonomously researches topics, stores knowledge in a vector database, retrieves relevant context, generates study notes, interview questions, quizzes, and allows users to upload PDF documents for AI-powered document analysis.

---

## ✨ Features

- 🧠 **Research Planning Agent**
  - Creates a structured research plan before starting research.

- 🌐 **Web Research Agent**
  - Collects information from multiple web sources using DuckDuckGo Search.

- 📚 **Retrieval-Augmented Generation (RAG)**
  - Converts research into vector embeddings.
  - Stores embeddings in Pinecone.
  - Retrieves relevant context for accurate AI responses.

- 📄 **Document Upload & Analysis**
  - Upload PDF documents.
  - Extract text using PyPDF.
  - Store document embeddings in Pinecone.
  - Generate AI-powered study notes from uploaded documents.

- 📝 **AI Study Notes Generator**
  - Creates detailed notes from retrieved knowledge.

- 💼 **Interview Question Generator**
  - Generates Basic, Intermediate, and Advanced interview questions.

- ❓ **Interactive Quiz Generator**
  - Generates multiple-choice questions with answers and explanations.

- 📄 **PDF Report Export**
  - Download complete AI-generated research reports.

- 📚 **Research History**
  - Stores research topics during the current session.

---

# 🧠 Agentic AI Workflow

```
                User Topic
                     │
                     ▼
          🧠 Research Planner Agent
                     │
                     ▼
         🌐 Web Research Agent
                     │
                     ▼
        📄 Information Collection
                     │
                     ▼
      ✂️ Document Chunking
                     │
                     ▼
      🔢 Sentence Embeddings
                     │
                     ▼
     📦 Pinecone Vector Database
                     │
                     ▼
        🔍 RAG Retrieval Agent
                     │
                     ▼
             🤖 Groq LLM
                     │
                     ▼
 Summary • Notes • Interview Questions
         Quiz • PDF Report
```

---

# 📄 Document RAG Workflow

```
Upload PDF
      │
      ▼
Extract Text (PyPDF)
      │
      ▼
Split into Chunks
      │
      ▼
Generate Embeddings
      │
      ▼
Store in Pinecone
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Groq LLM
      │
      ▼
Study Notes
Interview Questions
AI Responses
```

---

# 🚀 Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| UI Framework | Streamlit |
| Large Language Model | Groq (Llama 3.3 70B) |
| Vector Database | Pinecone |
| Embedding Model | SentenceTransformers |
| RAG Pipeline | Pinecone + Sentence Transformers |
| PDF Processing | PyPDF |
| Web Search | DuckDuckGo Search |
| Report Generation | ReportLab |

---

# 📦 Requirements

```
streamlit
groq
duckduckgo-search
reportlab
pinecone
sentence-transformers
pypdf
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Configuration

Create:

```
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY="your_groq_api_key"

PINECONE_API_KEY="your_pinecone_api_key"
```

---

# ▶️ Running the Application

```bash
streamlit run app.py
```

---

# 🧭 How to Use

### 🏠 Home
Overview of the AI Research Assistant.

### 🔍 Research
- Enter any research topic.
- AI creates a research plan.
- Searches the web.
- Stores knowledge in Pinecone.
- Retrieves relevant information using RAG.
- Generates AI summary.

### 📄 Upload PDF
- Upload any PDF document.
- Extracts document text.
- Creates embeddings.
- Stores vectors in Pinecone.
- Generates AI study notes from the uploaded document.

### 📝 Notes
Generates detailed notes using retrieved research context.

### 💼 Interview Questions
Creates Basic, Intermediate and Advanced interview questions.

### ❓ Quiz
Generates an interactive multiple-choice quiz.

### 📄 Download PDF
Download the complete AI-generated report.

---

# 📂 Project Structure

```
AI-Research-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit
    └── secrets.toml
```

---

# 🎯 Key Features

✅ Agentic AI Workflow

✅ Research Planning

✅ Multi-source Web Research

✅ Retrieval-Augmented Generation (RAG)

✅ Pinecone Vector Database

✅ Sentence Embeddings

✅ PDF Upload & AI Analysis

✅ AI Study Notes Generation

✅ Interview Question Generator

✅ Interactive Quiz

✅ PDF Report Export

---

# 🔮 Future Enhancements

- Support multiple document uploads.
- Research citations with source references.
- Voice-based AI assistant.
- Multi-agent collaboration.
- Research report comparison.
- Cloud deployment with authentication.

---

# 👩‍💻 Author

**Dharshini N**

B.Sc. Computer Science with Artificial Intelligence

GitHub:
https://github.com/dharshini-36

---

# 📜 License

This project is developed for educational, research, and portfolio purposes.
