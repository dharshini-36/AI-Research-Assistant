import streamlit as st
import os
import time
from datetime import datetime

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


if GROQ_API_KEY:

    client = Groq(
        api_key=GROQ_API_KEY
    )

else:

    client = None

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
"ℹ About"
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
    AI Planner
    →
    Research
    →
    Summary
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
# GEMINI RESPONSE FUNCTION
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
# INFORMATION COLLECTION AGENT
# ============================================================


def collect_information(topic):

    """
    Collects information from multiple searches
    """

    queries = [

        topic,

        topic + " explanation",

        topic + " applications",

        topic + " advantages and challenges"

    ]


    collected = []


    for q in queries:


        results = web_search(q)


        for item in results:

            collected.append(
                item
            )


    return collected





# ============================================================
# SUMMARY GENERATION AGENT
# ============================================================


def generate_summary(topic, information):

    """
    Converts collected information into summary
    """


    text = ""


    for item in information:

        text += (

            item["title"]
            +
            "\n"
            +
            item["body"]
            +
            "\n\n"

        )


    prompt = f"""


You are an AI summarization agent.


Research Topic:

{topic}


Collected Information:

{text}



Create a detailed summary containing:

1. Introduction

2. Definition

3. Main Concepts

4. Real World Applications

5. Advantages

6. Challenges

7. Future Scope



Make it easy for students to understand.


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
            # Step 1: Planning
            # --------------------------------------------


            with st.status(
                "🧠 AI Planner is creating research strategy...",
                expanded=True
            ) as status:


                plan = research_planner(
                    topic
                )


                st.write(
                    "✅ Research plan created"
                )


                status.update(
                    label="Research plan completed",
                    state="complete"
                )




            # --------------------------------------------
            # Step 2: Keyword Extraction
            # --------------------------------------------


            with st.status(
                "🔑 Finding important keywords..."
            ):


                keywords = extract_keywords(
                    topic
                )


                st.write(
                    keywords
                )




            # --------------------------------------------
            # Step 3: Web Research
            # --------------------------------------------


            with st.status(
                "🌐 Searching online resources..."
            ):


                information = collect_information(
                    topic
                )


                st.success(
                    f"{len(information)} resources collected"
                )




            # --------------------------------------------
            # Step 4: Summary Generation
            # --------------------------------------------


            with st.status(
                "✍️ AI is writing research summary..."
            ):


                summary = generate_summary(
                    topic,
                    information
                )



            # --------------------------------------------
            # Save Results
            # --------------------------------------------


            st.session_state.research_data = {


                "topic":
                topic,


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
            "🧠 AI Research Plan"
        )


        with st.expander(
            "View Research Plan"
        ):

            st.write(
                data["plan"]
            )



        st.subheader(
            "🔑 Keywords"
        )


        with st.expander(
            "View Keywords"
        ):

            st.write(
                data["keywords"]
            )



        st.subheader(
            "📝 AI Generated Summary"
        )


        st.write(
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



Generate:

- 5 Basic Questions

- 5 Intermediate Questions

- 5 Advanced Questions


Also provide short answers.


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

Format:


Question:

A)

B)

C)

D)


Correct Answer:


Explanation:



"""


    return ask_ai(prompt)




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


        st.write(
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



        st.write(
            data["interview"]
        )



    else:


        st.warning(
            "Please complete research first."
        )




# ============================================================
# QUIZ PAGE
# ============================================================


if page == "❓ Quiz":



    st.markdown(
    """
    <div class="card">

    <h2>
    ❓ AI Generated Quiz
    </h2>


    <p>
    Test your understanding using AI generated questions.
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


                quiz = generate_quiz(
                    data["topic"],
                    data["summary"]
                )


                data["quiz"] = quiz




        st.subheader(
            "🧠 Your Quiz"
        )



        st.write(
            data["quiz"]
        )



        st.divider()



        st.success(
            "Review the answers and explanations generated by AI."
        )



    else:


        st.warning(
            "Please complete research first."
        )

# ============================================================
# PART 5/5
# PDF GENERATION + FINAL PAGES
# ============================================================



# ============================================================
# PDF GENERATOR FUNCTION
# ============================================================


def create_pdf(content, filename="AI_Research_Report.pdf"):


    path = filename


    doc = SimpleDocTemplate(
        path
    )


    styles = getSampleStyleSheet()


    story = []



    for section in content.split("\n"):


        if section.strip():


            story.append(
                Paragraph(
                    section,
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


AI Research Assistant Report


Topic:

{data.get("topic","")}



Generated Time:

{data.get("time","")}



========================


RESEARCH PLAN


{data.get("plan","")}



========================


SUMMARY


{data.get("summary","")}



========================


STUDY NOTES


{data.get("notes","Not Generated")}



========================


INTERVIEW QUESTIONS


{data.get("interview","Not Generated")}



========================


QUIZ


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
# ABOUT PAGE
# ============================================================


if page == "ℹ About":



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

    <li>Google Gemini API</li>

    <li>DuckDuckGo Search</li>

    <li>ReportLab</li>

    <li>Generative AI</li>

    </ul>



    <h3>
    Agent Workflow
    </h3>


    <p>

    Planner Agent

    →

    Research Agent

    →

    Summary Agent

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

