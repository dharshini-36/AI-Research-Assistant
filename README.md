# 🤖 AI Research Assistant Agent

An Agentic AI-powered research assistant that autonomously researches topics, generates summaries, creates study notes, prepares interview questions, generates quizzes, and exports complete research reports as PDFs.

This project demonstrates **Agentic AI concepts** such as AI planning, tool usage, autonomous workflows, and multi-step reasoning.

---

# 🚀 Features

## 🧠 AI Research Planning Agent
- Understands user research topics
- Creates a structured research plan
- Identifies important concepts and keywords

## 🔎 Web Research Agent
- Searches online resources automatically
- Collects relevant information
- Processes multiple search results

## 📝 AI Summary Generator
- Converts collected information into structured summaries
- Generates easy-to-understand explanations
- Provides real-world applications and examples

## 📚 Study Notes Generator
Creates detailed learning material including:

- Definition
- Core concepts
- Workflow/Architecture
- Advantages
- Limitations
- Applications
- Future scope

## 💼 Interview Preparation Agent

Generates:

- Basic interview questions
- Intermediate questions
- Advanced technical questions
- Short explanations

## ❓ AI Quiz Generator

Creates:

- Multiple-choice questions
- Answers
- Explanations

## 📄 PDF Report Generation

Exports:

- Research plan
- Summary
- Study notes
- Interview questions
- Quiz

into a downloadable PDF report.

---

# 🏗️ Agent Workflow

```
User Topic

      ↓

AI Planning Agent

      ↓

Research Agent

      ↓

Information Collection

      ↓

Summary Agent

      ↓

Notes Generator

      ↓

Interview Agent

      ↓

Quiz Generator

      ↓

PDF Report
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Web application framework |
| Google Gemini API | Large Language Model |
| DuckDuckGo Search | Web information retrieval |
| ReportLab | PDF generation |
| Generative AI | AI content generation |

---

# 📂 Project Structure

```
AI-Research-Agent/

│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/your-username/AI-Research-Agent.git
```

## 2. Navigate to Project Folder

```bash
cd AI-Research-Agent
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Configuration

This project uses Google Gemini API.

Create Streamlit secrets:

```
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY="your_api_key_here"
```

For Streamlit Cloud:

Go to:

```
App Settings → Secrets
```

Add the same API key.

---

# ▶️ Run Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🎯 How It Works

1. Enter a research topic.
2. AI planner creates a research strategy.
3. Search agent collects information.
4. Gemini AI generates a summary.
5. Notes agent creates learning material.
6. Interview agent prepares questions.
7. Quiz agent tests understanding.
8. PDF generator creates a final report.

---

# 💡 Example Topics

You can research:

- Agentic AI
- Machine Learning
- Deep Learning
- Cloud Computing
- Blockchain
- Cybersecurity
- Generative AI
- Internet of Things

---

# 📸 Application Screens

(Add screenshots after deployment)

```
Home Page
Research Page
Notes Page
Quiz Page
PDF Download
```

---

# 🌟 Future Improvements

- Add long-term memory using vector databases
- Add chatbot conversation mode
- Add PDF/document upload support
- Add citation generation
- Add voice interaction
- Add multi-agent collaboration
- Add personalized learning recommendations

---

# 🧠 Agentic AI Concepts Demonstrated

This project demonstrates:

✅ AI Agents  
✅ Autonomous Task Execution  
✅ Planning and Reasoning  
✅ Tool Calling  
✅ LLM Integration  
✅ Information Retrieval  
✅ Content Generation  
✅ Workflow Automation  

---

# 👩‍💻 Author

**Dharshini N**

B.Sc Computer Science with Artificial Intelligence

---

# 📜 License

This project is created for educational and portfolio purposes.
