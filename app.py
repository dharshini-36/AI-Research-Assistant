import streamlit as st
import os
import re
import time
from datetime import datetime
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import uuid

# AI
from groq import Groq

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Search
from duckduckgo_search import DDGS


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Assistant Agent",
    page_icon="🤖",
    layout="wide"
)

try:

    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except:

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
try:

    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

except:

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


if GROQ_API_KEY:

    client = Groq(
        api_key=GROQ_API_KEY
    )

else:

    client = None
if PINECONE_API_KEY:
    pc = Pinecone(
        api_key=PINECONE_API_KEY
    )
    index = pc.Index("research-agent")
    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

else:

    index = None
    embedding_model = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
"""
<style>


/* Main Background */

.stApp{

background:
linear-gradient(
135deg,
#dbeafe,
#f0fdf4,
#fef3c7
);

}


/* Header */

.main-title{

font-size:42px;
font-weight:800;
text-align:center;

background:
linear-gradient(
90deg,
#2563eb,
#9333ea
);

-webkit-background-clip:text;
color:transparent;

margin-bottom:10px;

}


.subtitle{

text-align:center;
font-size:18px;
color:#374151;

}


/* Cards */


.card{

background:
rgba(255,255,255,0.75);

backdrop-filter:
blur(15px);

padding:25px;

border-radius:20px;

box-shadow:
0px 8px 30px rgba(0,0,0,0.12);

margin-bottom:20px;

}


/* Buttons */

.stButton button{

width:100%;

border-radius:15px;

height:45px;

font-size:16px;

font-weight:600;

background:
linear-gradient(
90deg,
#2563eb,
#9333ea
);

color:white;

border:none;

}


/* Text Area */

textarea{

border-radius:15px!important;

}


/* Sidebar */

section[data-testid="stSidebar"]{

background:
linear-gradient(
180deg,
#eff6ff,
#f5f3ff
);

}


/* ------------------------------------------------------------
   FIX: Streamlit's default white/boxy containers
   (expander, status widget, alerts) so they match the theme
   instead of showing as big flat white blocks.
------------------------------------------------------------ */

/* Expanders */
div[data-testid="stExpander"]{

background: rgba(255,255,255,0.65) !important;
border-radius: 16px !important;
border: 1px solid rgba(0,0,0,0.06) !important;
box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
overflow: hidden;

}

div[data-testid="stExpander"] summary{

background: transparent !important;
border-radius: 16px !important;
font-weight: 600;

}

div[data-testid="stExpanderDetails"]{

background: transparent !important;

}

/* st.status widget */
div[data-testid="stStatusWidget"]{

background: rgba(255,255,255,0.65) !important;
border-radius: 16px !important;
border: 1px solid rgba(0,0,0,0.06) !important;
box-shadow: 0px 4px 18px rgba(0,0,0,0.08);

}

/* st.info / st.success / st.warning / st.error */
div[data-testid="stAlert"]{

background: rgba(255,255,255,0.65) !important;
backdrop-filter: blur(10px);
border-radius: 16px !important;
box-shadow: 0px 4px 15px rgba(0,0,0,0.08);

}

/* Generic vertical block wrappers Streamlit sometimes paints white */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlock"]{

background: transparent !important;

}

/* Code / preformatted blocks inside AI outputs */
div[data-testid="stMarkdownContainer"] pre{

background: rgba(17,24,39,0.85) !important;
border-radius: 12px !important;

}


</style>

""",
unsafe_allow_html=True
)



# ============================================================
# SESSION MEMORY
# ============================================================


if "research_data" not in st.session_state:

    st.session_state.research_data = {}


if "history" not in st.session_state:

    st.session_state.history = []


if "quiz_answers" not in st.session_state:

    st.session_state.quiz_answers = {}


if "quiz_submitted" not in st.session_state:

    st.session_state.quiz_submitted = False


if "uploaded_docs" not in st.session_state:

    st.session_state.uploaded_docs = []


if "doc_qa_history" not in st.session_state:

    st.session_state.doc_qa_history = []


if "doc_notes" not in st.session_state:

    st.session_state.doc_notes = {}



# ============================================================
# HEADER
# ============================================================


st.markdown(
"""
<div class="main-title">

🤖 AI Research Assistant Agent

</div>


<div class="subtitle">

An autonomous AI agent that researches topics,
creates notes, generates quizzes and exports reports.

</div>

<br>

""",
unsafe_allow_html=True
)



# ============================================================
# SIDEBAR
# ============================================================


st.sidebar.title(
"🚀 Navigation"
)


page = st.sidebar.radio(
"Choose Section",
[
"🏠 Home",
"🔍 Research",
"📝 Notes",
"❓ Quiz",
"📄 Download PDF",
"📎 Document Q&A",
"About"
]
)



st.sidebar.markdown("---")


st.sidebar.info(
"""
### Agent Capabilities

🔎 Web Research

🧠 AI Reasoning

📝 Notes Generation

❓ Quiz Creation

📄 PDF Reports

"""
)


# ============================================================
# TEXT FORMATTING HELPER
# ============================================================
#
# Turns raw AI text into markdown where:
#   - "Question:" / "Q1:" style lines are bold
#   - "Answer:" / "Correct Answer:" lines are bold and pushed
#     onto their own line right after the question
#   - "Explanation:" lines are italic
#   - numbered section headings ("1. Definition") become subheadings
#
# This fixes the issue of everything being dumped as one big
# undifferentiated paragraph via st.write().

QUESTION_PATTERN = re.compile(r'^(Q(?:uestion)?\s*\.?\s*#?\d*\s*[:.\-]?)\s*(.*)$', re.IGNORECASE)
ANSWER_PATTERN = re.compile(r'^(Correct\s+Answer|Answer)\s*[:.\-]\s*(.*)$', re.IGNORECASE)
EXPLANATION_PATTERN = re.compile(r'^(Explanation)\s*[:.\-]\s*(.*)$', re.IGNORECASE)
OPTION_PATTERN = re.compile(r'^[A-D][\).:]\s*(.*)$')
HEADING_PATTERN = re.compile(r'^(\d+)\.\s+([A-Z][a-zA-Z /\-]{2,40})$')


def format_ai_text(text: str) -> str:

    if not text or not text.strip():
        return "_No content generated yet._"

    lines = text.split("\n")
    output = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            output.append("")
            continue

        q_match = QUESTION_PATTERN.match(line)
        a_match = ANSWER_PATTERN.match(line)
        e_match = EXPLANATION_PATTERN.match(line)
        o_match = OPTION_PATTERN.match(line)
        h_match = HEADING_PATTERN.match(line)

        if q_match:
            label, rest = q_match.groups()
            output.append("")
            output.append(f"**{label.strip()} {rest}**".strip())

        elif a_match:
            label, rest = a_match.groups()
            output.append(f"**{label.strip()}:** {rest}".strip())

        elif e_match:
            label, rest = e_match.groups()
            output.append(f"*{label.strip()}: {rest}*".strip())

        elif o_match:
            output.append(f"&nbsp;&nbsp;{line}")

        elif h_match:
            num, title = h_match.groups()
            output.append("")
            output.append(f"#### {num}. {title}")

        else:
            output.append(line)

    # Force real markdown line breaks (two trailing spaces) between lines
    return "  \n".join(output)


def render_ai_block(text: str):
    st.markdown(format_ai_text(text))


# ============================================================
# HOME PAGE
# ============================================================


if page == "🏠 Home":


    st.markdown(
    """

    <div class="card">


    <h2>
    Welcome to AI Research Assistant
    </h2>


    <p>

    This application uses Agentic AI concepts.
    Instead of only answering questions,
    the AI plans tasks, collects information,
    summarizes knowledge and creates learning material.

    </p>


    <h3>
    Workflow
    </h3>


    <p>

    User Topic
    →
    Manager Agent
    →
    Planner
    →
    Research
    →
    Summary
    →
    Critic
    →
    Notes
    →
    Quiz
    →
    PDF

    </p>


    </div>

    """,
    unsafe_allow_html=True
    )


    st.success(
        "Start by going to the Research section from the sidebar."
    )


# ============================================================
# GROQ RESPONSE FUNCTION
# ============================================================

def ask_ai(prompt):
    if client is None:
        return "⚠️ Groq API key not configured."


    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7

        )


        return response.choices[0].message.content


    except Exception as e:

        return f"Groq Error: {str(e)}"

# ============================================================
# CREATE EMBEDDING
# ============================================================

def create_embedding(text):

    if embedding_model is None:

        return None

    return embedding_model.encode(text).tolist()


# ============================================================
# STORE DATA IN PINECONE
# ============================================================

def store_in_pinecone(topic, text, extra_metadata=None):

    if index is None:

        return

    vector = create_embedding(text)

    if vector is None:

        return

    metadata = {

        "topic": topic,

        "text": text,

        "type": "research_memory"

    }

    if extra_metadata:

        metadata.update(extra_metadata)

    index.upsert(

        vectors=[

            {

                "id": str(uuid.uuid4()),

                "values": vector,

                "metadata": metadata

            }

        ]

    )


# ============================================================
# RETRIEVE DATA FROM PINECONE
# ============================================================
#
# `filter_dict` lets a caller restrict retrieval to a metadata subset
# — e.g. {"doc_name": "resume.pdf", "type": "uploaded_document"} so a
# document Q&A query only pulls chunks from that specific PDF instead
# of mixing in unrelated research memory.

def retrieve_from_pinecone(query, top_k=5, filter_dict=None):

    if index is None:

        return ""

    vector = create_embedding(query)

    if vector is None:

        return ""

    query_kwargs = {

        "vector": vector,

        "top_k": top_k,

        "include_metadata": True

    }

    if filter_dict:

        query_kwargs["filter"] = filter_dict

    results = index.query(**query_kwargs)

    context = ""

    for match in results["matches"]:

        context += match["metadata"]["text"] + "\n\n"

    return context
# ============================================================
# PDF KNOWLEDGE BASE AGENT
# ============================================================

def extract_pdf_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ============================================================
# SPLIT DOCUMENT INTO CHUNKS
# ============================================================

def split_document(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=800,

        chunk_overlap=100

    )

    return splitter.split_text(text)


# ============================================================
# STORE PDF INTO PINECONE
# ============================================================

def upload_pdf_to_pinecone(uploaded_file):

    if uploaded_file is None:

        return 0

    text = extract_pdf_text(uploaded_file)

    chunks = split_document(text)

    for chunk in chunks:

        store_in_pinecone(

            uploaded_file.name,

            chunk,

            extra_metadata={

                "doc_name": uploaded_file.name,

                "type": "uploaded_document"

            }

        )

    return len(chunks)


# ============================================================
# DOCUMENT Q&A AGENT (RAG over a single uploaded PDF)
# ============================================================
#
# Retrieves ONLY chunks belonging to the selected document
# (via the doc_name + type filter) and instructs the model to
# answer strictly from that context — not from general knowledge
# or from other topics/documents stored in Pinecone.

def answer_from_document(question, doc_name, top_k=5):

    if index is None:

        return "⚠️ Pinecone is not configured, so document Q&A is unavailable."

    context = retrieve_from_pinecone(

        question,

        top_k=top_k,

        filter_dict={

            "doc_name": doc_name,

            "type": "uploaded_document"

        }

    )

    if not context.strip():

        return "I couldn't find anything relevant to that question in this document."

    prompt = f"""

You are a Document Q&A Agent. Answer the question using ONLY the
context below, which was retrieved from the uploaded document
"{doc_name}". Do not use any outside knowledge.

If the answer is not contained in the context, reply exactly:
"This isn't covered in the uploaded document."

Context:
{context}

Question:
{question}

Answer:

"""

    return ask_ai(prompt)


# ============================================================
# DOCUMENT CONTEXT RETRIEVAL (for full-document tasks like Notes)
# ============================================================
#
# Notes/summaries need broad coverage of the document rather than
# the handful of chunks most similar to a single question. This
# pulls back a much larger, deduplicated slice of the document's
# stored chunks (still scoped to that doc_name via the filter) so
# the notes generator has enough material to work from.

def get_full_document_context(doc_name, top_k=40):

    if index is None:

        return ""

    # A generic/broad query (the document name itself) combined with
    # a high top_k pulls back a wide spread of the document's chunks.
    context = retrieve_from_pinecone(

        doc_name,

        top_k=top_k,

        filter_dict={

            "doc_name": doc_name,

            "type": "uploaded_document"

        }

    )

    return context


# ============================================================
# DOCUMENT NOTES AGENT (study notes generated from an uploaded doc)
# ============================================================

def generate_notes_from_document(doc_name):

    if index is None:

        return "⚠️ Pinecone isn't configured, so document notes are unavailable."

    context = get_full_document_context(doc_name)

    if not context.strip():

        return "I couldn't find any indexed content for this document."

    prompt = f"""

You are an AI Study Notes Generator.

Create detailed, well-structured study notes using ONLY the content
below, which was extracted from the uploaded document "{doc_name}".
Do not use any outside knowledge and do not invent information that
isn't supported by the content.

Document Content:
{context}

Create the notes with these sections (skip a section only if the
document truly has nothing relevant to it):

1. Overview / Summary
2. Key Concepts & Definitions
3. Important Points (as a bullet list)
4. Key Facts, Figures & Data
5. Conclusion / Takeaways

Keep the notes clear, concise and easy to study from.

"""

    return ask_ai(prompt)


# ============================================================
# MANAGER AGENT
# ============================================================
#
# Decides the execution plan before any other agent runs. This is
# what makes the pipeline "agentic" rather than a fixed script — the
# plan text is generated by the LLM based on the topic, and is shown
# to the user for transparency. (Other agents currently always run
# regardless of this plan's content — the plan is advisory/explanatory
# for now, not yet used to branch execution.)


def manager_agent(topic):

    prompt = f"""

You are an AI Manager Agent coordinating a team of research agents.

Topic:
{topic}

Decide the execution plan for researching this topic. List, in order,
which of the following steps are needed and briefly why:

1. Research Planning
2. Keyword Extraction
3. Knowledge Retrieval / Web Search
4. Summary Generation
5. Critic Review (only if the topic is broad or complex)
6. Memory Storage

Return a short, numbered execution plan.

"""

    return ask_ai(prompt)


# ============================================================
# RESEARCH PLANNER AGENT
# ============================================================


def research_planner(topic):

    """
    AI decides what information is required
    """

    prompt = f"""

You are an AI Research Planning Agent.

Create a research plan for this topic:

Topic:
{topic}


Generate:

1. Important concepts to study
2. Key questions to answer
3. Important keywords for searching
4. Expected output structure


Return the plan in a structured format.

"""


    return ask_ai(prompt)

# ============================================================
# WEB SEARCH AGENT
# ============================================================


def web_search(query, limit=5):

    """
    Searches internet using DuckDuckGo
    """

    results = []


    try:

        with DDGS() as ddgs:


            search_results = ddgs.text(
                query,
                max_results=limit
            )


            for result in search_results:


                results.append(
                    {
                    "title":
                    result.get("title"),

                    "body":
                    result.get("body"),

                    "link":
                    result.get("href")
                    }
                )


    except Exception as e:

        results.append(
            {
            "title":"Search Error",
            "body":str(e),
            "link":""
            }
        )


    return results

# ============================================================
# INFORMATION COLLECTION AGENT (RAG + WEB SEARCH)
# ============================================================

def collect_information(topic):

    """
    Agent Workflow

    1. Search Pinecone Knowledge Base
    2. If enough knowledge exists, use it.
    3. Otherwise search DuckDuckGo.
    4. Store new knowledge inside Pinecone.
    """

    collected = []

    # -----------------------------------------
    # STEP 1 : Retrieve Existing Knowledge
    # -----------------------------------------

    context = retrieve_from_pinecone(topic)

    if context.strip():

        collected.append(
            {
                "title": "Knowledge Base",
                "body": context,
                "link": "Pinecone Vector Database"
            }
        )

        return collected

    # -----------------------------------------
    # STEP 2 : Search the Web
    # -----------------------------------------

    queries = [

        topic,

        topic + " explanation",

        topic + " applications",

        topic + " advantages",

        topic + " challenges",

        topic + " future scope"

    ]

    for query in queries:

        results = web_search(query)

        for item in results:

            collected.append(item)

            text = f"""

Title:
{item['title']}

Content:
{item['body']}

Source:
{item['link']}

"""

            store_in_pinecone(
                topic,
                text
            )

    return collected
# ============================================================
# RAG SUMMARY GENERATION AGENT
# ============================================================

def generate_summary(topic, information):

    """
    Generates a research summary using
    both Pinecone knowledge and
    latest web search results.
    """

    # -----------------------------------------
    # Retrieve Knowledge from Pinecone
    # -----------------------------------------

    retrieved_context = retrieve_from_pinecone(topic)

    # -----------------------------------------
    # Prepare Latest Web Information
    # -----------------------------------------

    web_information = ""

    for item in information:

        web_information += f"""

Title:
{item['title']}

Content:
{item['body']}

Source:
{item['link']}

"""

    # -----------------------------------------
    # Prompt
    # -----------------------------------------

    prompt = f"""

You are an intelligent Research Summary Agent.

Use BOTH sources below.

=========================
Knowledge Base (Pinecone)
=========================

{retrieved_context}

=========================
Latest Web Search
=========================

{web_information}

Your tasks:

1. Combine both sources.

2. Remove duplicate information.

3. Give priority to the most recent information.

4. Create a detailed report containing:

• Introduction

• Definition

• Core Concepts

• Architecture / Workflow

• Applications

• Advantages

• Challenges

• Future Scope

• Conclusion

Make the explanation simple enough for students while still suitable for technical interviews.

"""

    summary = ask_ai(prompt)

    # -----------------------------------------
    # Store Final Summary
    # -----------------------------------------

    store_in_pinecone(
        topic,
        summary
    )

    return summary
# ============================================================
# MEMORY AGENT
# ============================================================

def memory_agent(topic, summary, keywords):

    memory = f"""

Topic:
{topic}

Keywords:
{keywords}

Summary:
{summary}

"""

    store_in_pinecone(
        f"memory_{topic}",
        memory
    )


# ============================================================
# CRITIC AGENT
# ============================================================

def critic_agent(topic, summary):

    prompt = f"""

You are an AI Critic Agent.

Review the following research summary.

Topic:
{topic}

Summary:

{summary}

Your tasks:

1. Check whether the summary is complete.

2. Check whether it contains:

- Definition

- Core Concepts

- Applications

- Advantages

- Challenges

- Future Scope

3. If something important is missing,
reply ONLY with:

YES

followed by the missing topics.

Otherwise reply ONLY:

NO

"""

    return ask_ai(prompt)
# ============================================================
# KEYWORD EXTRACTION AGENT
# ============================================================


def extract_keywords(topic):


    prompt = f"""


Extract important keywords related to:

{topic}


Return only a bullet list of keywords.


"""


    return ask_ai(prompt)


# ============================================================
# RESEARCH PAGE
# ============================================================


if page == "🔍 Research":


    st.markdown(
    """
    <div class="card">

    <h2>
    🔍 AI Research Agent
    </h2>

    <p>
    Enter a topic and the AI agent will automatically
    plan research, collect information, and generate
    a structured summary.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    topic = st.text_input(
        "Enter Research Topic",
        placeholder="Example: Agentic AI, Quantum Computing, Blockchain"
    )



    if st.button("🚀 Start Research"):


        if topic.strip() == "":


            st.warning(
                "Please enter a research topic."
            )


        else:

            # --------------------------------------------
            # MANAGER AGENT
            # --------------------------------------------

            with st.status(
                "🤖 Manager Agent is planning the workflow...",
                expanded=True
            ):

                workflow = manager_agent(topic)

                render_ai_block(workflow)

                st.success(
                    "Execution plan created."
                )

            # --------------------------------------------
            # PLANNER AGENT
            # --------------------------------------------

            with st.status(
                "🧠 Planner Agent is preparing the research..."
            ):

                plan = research_planner(topic)

            # --------------------------------------------
            # KEYWORD AGENT
            # --------------------------------------------

            with st.status(
                "🔑 Extracting keywords..."
            ):

                keywords = extract_keywords(topic)

            # --------------------------------------------
            # RETRIEVAL + WEB RESEARCH AGENT
            # --------------------------------------------

            with st.status(
                "📚 Retrieving knowledge..."
            ):

                information = collect_information(topic)

                st.success(
                    f"{len(information)} source(s) collected"
                )

            # --------------------------------------------
            # SUMMARY AGENT
            # --------------------------------------------

            with st.status(
                "📝 Generating summary..."
            ):

                summary = generate_summary(
                    topic,
                    information
                )

            # --------------------------------------------
            # CRITIC AGENT
            # --------------------------------------------

            with st.status(
                "🔍 Reviewing research..."
            ):

                review = critic_agent(
                    topic,
                    summary
                )

                if review.upper().startswith("YES"):

                    extra_information = collect_information(
                        topic + " latest trends"
                    )

                    summary = generate_summary(
                        topic,
                        information + extra_information
                    )

                    st.info(
                        "Critic Agent found gaps — summary was expanded."
                    )

                else:

                    st.success(
                        "Critic Agent approved the summary."
                    )

            # --------------------------------------------
            # MEMORY AGENT
            # --------------------------------------------

            memory_agent(
                topic,
                summary,
                keywords
            )

            # --------------------------------------------
            # SAVE RESULTS
            # --------------------------------------------

            st.session_state.research_data = {

                "topic":
                topic,

                "workflow":
                workflow,

                "plan":
                plan,

                "keywords":
                keywords,

                "information":
                information,

                "summary":
                summary,

                "time":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )

            }

            st.session_state.history.append(
                topic
            )

            # New topic → reset any previous quiz progress
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False

            st.success(
                "🎉 Research completed successfully!"
            )



    # --------------------------------------------
    # Display Previous Result
    # --------------------------------------------


    if st.session_state.research_data:



        data = st.session_state.research_data


        st.markdown(
        """
        <div class="card">

        <h2>
        📌 Research Result
        </h2>

        </div>
        """,
        unsafe_allow_html=True
        )



        st.subheader(
            "📚 Topic"
        )


        st.write(
            data["topic"]
        )


        st.subheader(
            "🤖 Manager Agent Execution Plan"
        )


        with st.expander(
            "View Execution Plan"
        ):

            render_ai_block(
                data.get("workflow", "")
            )



        st.subheader(
            "🧠 AI Research Plan"
        )


        with st.expander(
            "View Research Plan"
        ):

            render_ai_block(
                data["plan"]
            )



        st.subheader(
            "🔑 Keywords"
        )


        with st.expander(
            "View Keywords"
        ):

            render_ai_block(
                data["keywords"]
            )



        st.subheader(
            "📝 AI Generated Summary"
        )


        render_ai_block(
            data["summary"]
        )



        st.caption(
            "Generated on: "
            +
            data["time"]
        )


# ============================================================
# PART 4/5
# KNOWLEDGE GENERATION AGENTS
# ============================================================



# ============================================================
# STUDY NOTES GENERATOR AGENT
# ============================================================


def generate_notes(topic, summary):

    prompt = f"""

You are an AI Study Notes Generator.

Create detailed study notes for:

Topic:
{topic}


Based on this summary:

{summary}


Create notes with:

1. Definition

2. Core Concepts

3. Architecture / Workflow

4. Advantages

5. Limitations

6. Real World Examples

7. Applications

8. Future Scope


Make the notes suitable for students
and technical interviews.


"""


    return ask_ai(prompt)




# ============================================================
# INTERVIEW QUESTION GENERATOR AGENT
# ============================================================


def generate_interview_questions(topic, summary):


    prompt = f"""


You are an AI Interview Preparation Agent.


Generate interview questions for:

Topic:
{topic}


Information:

{summary}



Generate 15 questions total: 5 Basic, 5 Intermediate, 5 Advanced.

You MUST format EVERY question and answer exactly like this,
with nothing else on the "Question" or "Answer" lines:

Question: <the question text>
Answer: <a short, direct answer>

Question: <the question text>
Answer: <a short, direct answer>

(repeat for all 15 questions, grouped in order Basic -> Intermediate -> Advanced)

Do not number the questions yourself and do not add extra commentary
outside of the Question/Answer pairs.


"""


    return ask_ai(prompt)




# ============================================================
# QUIZ GENERATOR AGENT
# ============================================================


def generate_quiz(topic, summary):


    prompt = f"""


You are an AI Quiz Master.


Create a multiple-choice quiz.

Topic:

{topic}


Information:

{summary}



Generate 5 MCQ questions.

Format each one EXACTLY like this, with nothing else on the
"Question", "Correct Answer" or "Explanation" lines:

Question: <question text>
A) <option>
B) <option>
C) <option>
D) <option>
Correct Answer: <letter only, e.g. B>
Explanation: <one short sentence>

Leave a blank line between each question.


"""


    return ask_ai(prompt)


# ============================================================
# QUIZ PARSER
# ============================================================
#
# Turns the raw AI quiz text into a list of structured
# question dicts so the quiz can be rendered as real,
# clickable multiple-choice questions instead of plain text.
#
# Each item: {"question": str, "options": [(label, text), ...],
#             "correct": "A"/"B"/"C"/"D", "explanation": str}


def parse_quiz(quiz_text: str):

    if not quiz_text or not quiz_text.strip():
        return []

    blocks = re.split(r'\n\s*\n', quiz_text.strip())

    questions = []

    for block in blocks:

        q_match = re.search(r'Question\s*[:.\-]\s*(.+)', block, re.IGNORECASE)
        option_matches = re.findall(r'^[ \t]*([A-D])[\).:]\s*(.+)$', block, re.MULTILINE)
        ans_match = re.search(r'Correct\s+Answer\s*[:.\-]\s*([A-D])', block, re.IGNORECASE)
        exp_match = re.search(r'Explanation\s*[:.\-]\s*(.+)', block, re.IGNORECASE)

        if q_match and len(option_matches) >= 2 and ans_match:

            questions.append(
                {
                    "question": q_match.group(1).strip(),
                    "options": [(label.upper(), text.strip()) for label, text in option_matches],
                    "correct": ans_match.group(1).strip().upper(),
                    "explanation": exp_match.group(1).strip() if exp_match else ""
                }
            )

    return questions


# ============================================================
# NOTES PAGE
# ============================================================


if page == "📝 Notes":


    st.markdown(
    """
    <div class="card">

    <h2>
    📝 AI Study Notes Generator
    </h2>

    <p>
    Converts research information into structured
    learning material.
    </p>

    </div>

    """,
    unsafe_allow_html=True
    )



    if st.session_state.research_data:


        data = st.session_state.research_data



        if "notes" not in data:


            with st.spinner(
                "✍️ Creating detailed notes..."
            ):


                notes = generate_notes(
                    data["topic"],
                    data["summary"]
                )


                data["notes"] = notes



        st.subheader(
            "📚 Detailed Notes"
        )


        render_ai_block(
            data["notes"]
        )



        st.divider()



        st.subheader(
            "💼 Interview Questions"
        )



        if "interview" not in data:


            with st.spinner(
                "Preparing interview questions..."
            ):


                interview = generate_interview_questions(
                    data["topic"],
                    data["summary"]
                )


                data["interview"] = interview



        render_ai_block(
            data["interview"]
        )



    else:


        st.warning(
            "Please complete research first."
        )




# ============================================================
# QUIZ PAGE (interactive)
# ============================================================


if page == "❓ Quiz":



    st.markdown(
    """
    <div class="card">

    <h2>
    ❓ AI Generated Quiz
    </h2>


    <p>
    Answer each question, then submit to see your score,
    the correct answers, and the explanations.
    </p>


    </div>

    """,
    unsafe_allow_html=True
    )




    if st.session_state.research_data:


        data = st.session_state.research_data



        if "quiz" not in data:


            with st.spinner(
                "🤖 Creating quiz questions..."
            ):


                data["quiz"] = generate_quiz(
                    data["topic"],
                    data["summary"]
                )


        if "quiz_parsed" not in data:

            data["quiz_parsed"] = parse_quiz(data["quiz"])


        quiz_questions = data["quiz_parsed"]


        st.subheader(
            "🧠 Your Quiz"
        )


        if not quiz_questions:

            st.warning(
                "Couldn't read the quiz as structured questions, "
                "showing the raw AI output instead."
            )

            render_ai_block(
                data["quiz"]
            )


        else:

            submitted = st.session_state.quiz_submitted


            for i, q in enumerate(quiz_questions):


                st.markdown(f"**Q{i + 1}. {q['question']}**")


                option_display = [
                    f"{label}) {text}" for label, text in q["options"]
                ]


                selected_display = st.radio(
                    "Choose an answer",
                    option_display,
                    index=None,
                    key=f"quiz_choice_{i}",
                    disabled=submitted,
                    label_visibility="collapsed"
                )


                if selected_display and not submitted:

                    st.session_state.quiz_answers[i] = selected_display[0]


                if submitted:

                    user_letter = st.session_state.quiz_answers.get(i)
                    correct_letter = q["correct"]


                    if user_letter == correct_letter:

                        st.success(
                            f"✅ Correct — Answer: {correct_letter}"
                        )

                    else:

                        st.error(
                            f"❌ Your answer: {user_letter or 'Not answered'}"
                            f"  |  Correct answer: {correct_letter}"
                        )


                    if q["explanation"]:

                        st.info(
                            f"💡 {q['explanation']}"
                        )


                st.divider()



            if not submitted:


                if st.button("✅ Submit Quiz"):

                    st.session_state.quiz_submitted = True

                    st.rerun()


            else:


                score = sum(
                    1
                    for i, q in enumerate(quiz_questions)
                    if st.session_state.quiz_answers.get(i) == q["correct"]
                )


                st.success(
                    f"🎯 You scored {score} / {len(quiz_questions)}"
                )


                if st.button("🔄 Retake Quiz"):

                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_answers = {}

                    st.rerun()



    else:


        st.warning(
            "Please complete research first."
        )

# ============================================================
# PART 5/5
# PDF GENERATION + FINAL PAGES
# ============================================================



# ============================================================
# MARKDOWN -> REPORTLAB MARKUP HELPER
# ============================================================
#
# The AI output contains lightweight markdown (**bold**, ## headings,
# etc). ReportLab's Paragraph does NOT render markdown — it renders a
# small XML-like markup instead. Without conversion, the raw "**" and
# "##" characters show up literally in the PDF. This converts the
# markdown into ReportLab-friendly markup / styles.


def escape_for_reportlab(text: str) -> str:

    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def markdown_inline_to_reportlab(text: str) -> str:

    text = escape_for_reportlab(text)

    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # *italic* (single asterisks not already consumed above)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)

    return text


def create_pdf(content, filename="AI_Research_Report.pdf"):

    path = filename

    doc = SimpleDocTemplate(
        path
    )

    styles = getSampleStyleSheet()

    story = []


    heading_style_for_level = {
        1: "Heading1",
        2: "Heading1",
        3: "Heading2",
        4: "Heading3",
    }


    for raw_line in content.split("\n"):

        line = raw_line.strip()

        if not line:

            story.append(
                Spacer(1, 6)
            )

            continue


        # Skip plain "====" style dividers, replaced by heading spacing
        if re.match(r'^=+$', line):

            continue


        heading_match = re.match(r'^(#{1,4})\s+(.*)$', line)


        if heading_match:

            hashes, title = heading_match.groups()

            level = len(hashes)

            style_name = heading_style_for_level.get(level, "Heading2")

            story.append(
                Paragraph(
                    markdown_inline_to_reportlab(title.strip()),
                    styles[style_name]
                )
            )

            story.append(
                Spacer(1, 10)
            )

            continue


        story.append(
            Paragraph(
                markdown_inline_to_reportlab(line),
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(
                1,
                12
            )
        )



    doc.build(
        story
    )


    return path





# ============================================================
# CREATE COMPLETE REPORT
# ============================================================


def prepare_report(data):


    report = f"""

# AI Research Assistant Report


**Topic:** {data.get("topic","")}

**Generated Time:** {data.get("time","")}


## Manager Agent Execution Plan

{data.get("workflow","Not Generated")}


## Research Plan

{data.get("plan","")}


## Summary

{data.get("summary","")}


## Study Notes

{data.get("notes","Not Generated")}


## Interview Questions

{data.get("interview","Not Generated")}


## Quiz

{data.get("quiz","Not Generated")}

"""


    return report





# ============================================================
# DOWNLOAD PDF PAGE
# ============================================================


if page == "📄 Download PDF":



    st.markdown(
    """

    <div class="card">

    <h2>
    📄 Download Research Report
    </h2>


    <p>

    Export your AI generated research,
    notes, interview questions and quiz
    into a PDF document.

    </p>


    </div>

    """,

    unsafe_allow_html=True
    )



    if st.session_state.research_data:



        data = st.session_state.research_data



        if "notes" not in data:


            with st.spinner(
                "Preparing notes..."
            ):


                data["notes"] = generate_notes(
                    data["topic"],
                    data["summary"]
                )



        if "interview" not in data:


            data["interview"] = generate_interview_questions(
                data["topic"],
                data["summary"]
            )



        if "quiz" not in data:


            data["quiz"] = generate_quiz(
                data["topic"],
                data["summary"]
            )



        report = prepare_report(
            data
        )



        pdf_file = create_pdf(
            report
        )



        with open(
            pdf_file,
            "rb"
        ) as file:


            st.download_button(

                label="⬇️ Download PDF Report",

                data=file,

                file_name="AI_Research_Report.pdf",

                mime="application/pdf"

            )



    else:


        st.warning(
            "Please complete research before downloading."
        )


# ============================================================
# DOCUMENT Q&A PAGE
# ============================================================


if page == "📎 Document Q&A":


    st.markdown(
    """
    <div class="card">

    <h2>
    📎 Chat With Your Document
    </h2>

    <p>
    Upload a PDF, let the agent read and index it, then ask
    questions that are answered strictly from that document
    (retrieval-augmented generation) — not from general knowledge.
    You can also generate study notes straight from the document.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    if index is None:

        st.warning(
            "Pinecone isn't configured (PINECONE_API_KEY missing), "
            "so document upload and Q&A are unavailable."
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload a PDF",
            type=["pdf"]
        )

        if uploaded_file is not None:

            already_processed = uploaded_file.name in st.session_state.uploaded_docs

            if already_processed:

                st.info(
                    f"'{uploaded_file.name}' is already indexed. "
                    "You can ask questions or generate notes below."
                )

            else:

                if st.button("📥 Process & Index Document"):

                    with st.spinner(
                        "Extracting text and storing chunks in Pinecone..."
                    ):

                        chunk_count = upload_pdf_to_pinecone(uploaded_file)

                    if chunk_count:

                        st.session_state.uploaded_docs.append(uploaded_file.name)

                        st.success(
                            f"Indexed '{uploaded_file.name}' as {chunk_count} chunk(s)."
                        )

                    else:

                        st.error(
                            "No extractable text was found in this PDF "
                            "(it may be a scanned/image-only document)."
                        )

        st.divider()

        if not st.session_state.uploaded_docs:

            st.caption(
                "No documents indexed yet. Upload a PDF above to get started."
            )

        else:

            selected_doc = st.selectbox(
                "Choose a document",
                st.session_state.uploaded_docs
            )

            # --------------------------------------------
            # DOCUMENT NOTES AGENT (UI)
            # --------------------------------------------

            st.subheader("📝 Study Notes From This Document")

            col_gen, col_regen = st.columns([1, 1])

            with col_gen:

                generate_clicked = st.button(
                    "✨ Generate Notes",
                    key="gen_doc_notes_btn"
                )

            with col_regen:

                regenerate_clicked = False

                if selected_doc in st.session_state.doc_notes:

                    regenerate_clicked = st.button(
                        "🔄 Regenerate Notes",
                        key="regen_doc_notes_btn"
                    )

            if generate_clicked or regenerate_clicked:

                with st.spinner(
                    f"Reading '{selected_doc}' and writing notes..."
                ):

                    st.session_state.doc_notes[selected_doc] = generate_notes_from_document(
                        selected_doc
                    )

            if selected_doc in st.session_state.doc_notes:

                render_ai_block(
                    st.session_state.doc_notes[selected_doc]
                )

                notes_pdf_path = create_pdf(
                    st.session_state.doc_notes[selected_doc],
                    filename=f"{selected_doc}_notes.pdf"
                )

                with open(notes_pdf_path, "rb") as notes_file:

                    st.download_button(

                        label="⬇️ Download Notes as PDF",

                        data=notes_file,

                        file_name=f"{selected_doc}_notes.pdf",

                        mime="application/pdf",

                        key="download_doc_notes_btn"

                    )

            else:

                st.caption(
                    "Click 'Generate Notes' to create study notes from this document."
                )

            st.divider()

            # --------------------------------------------
            # DOCUMENT Q&A (existing)
            # --------------------------------------------

            st.subheader("💬 Ask a Question")

            question = st.text_input(
                "Your question",
                placeholder="e.g. What does this document say about pricing?"
            )

            if st.button("🔎 Get Answer"):

                if question.strip() == "":

                    st.warning("Please enter a question.")

                else:

                    with st.spinner("Searching the document..."):

                        answer = answer_from_document(
                            question,
                            selected_doc
                        )

                    st.session_state.doc_qa_history.append(
                        {
                            "doc": selected_doc,
                            "question": question,
                            "answer": answer
                        }
                    )

            if st.session_state.doc_qa_history:

                st.subheader("📜 Q&A History")

                for entry in reversed(st.session_state.doc_qa_history):

                    st.markdown(f"**📎 {entry['doc']}**")

                    st.markdown(f"**Q:** {entry['question']}")

                    render_ai_block(entry["answer"])

                    st.divider()





# ============================================================
# ABOUT PAGE
# ============================================================


if page == "About":



    st.markdown(
    """

    <div class="card">


    <h2>
    🤖 About AI Research Assistant Agent
    </h2>


    <p>


    This project demonstrates Agentic AI concepts
    where AI can plan tasks, use external tools,
    process information and generate useful outputs.


    </p>



    <h3>
    Technologies Used
    </h3>


    <ul>

    <li>Python</li>

    <li>Streamlit</li>

    <li>Groq API</li>

    <li>DuckDuckGo Search</li>

    <li>Pinecone (vector memory / RAG)</li>

    <li>Sentence-Transformers (embeddings)</li>

    <li>ReportLab</li>

    <li>Generative AI</li>

    </ul>



    <h3>
    Agent Workflow
    </h3>


    <p>

    Manager Agent

    →

    Planner Agent

    →

    Keyword Agent

    →

    Retrieval / Research Agent

    →

    Summary Agent

    →

    Critic Agent

    →

    Memory Agent

    →

    Notes Agent

    →

    Quiz Agent

    </p>


    </div>


    """,

    unsafe_allow_html=True
    )



# ============================================================
# RESEARCH HISTORY DISPLAY
# ============================================================


with st.sidebar:


    st.markdown(
        "---"
    )


    st.subheader(
        "📚 Research History"
    )



    if st.session_state.history:


        for item in st.session_state.history:


            st.write(
                "• " + item
            )


    else:


        st.caption(
            "No research yet"
        )



# ============================================================
# FOOTER
# ============================================================


st.markdown(
"""

<br>

<center>

<p style="color:#6b7280;">

Built with ❤️ using Agentic AI + Streamlit

</p>

</center>


""",

unsafe_allow_html=True
)
