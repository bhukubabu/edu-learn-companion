import streamlit as st
import os
import random
import json
import time
import pandas as pd


# -------------------- Page Setup ---------------------
st.set_page_config(page_icon="", page_title="Study Booster", layout="centered", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            width: 750px !important;
        }
    </style>
    """, unsafe_allow_html=True)


from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType
#from langchain_community.chat_models import ChatGoogleGenerativeAI
from langchain.agents import Tool


import ques
import prompts
import quiz
import gen_qs
import model_
import summary
import map_data
from pptx import Presentation
from create_pdf import extract_pdf_text, extract_ppt_text, split_text



# -------------------- File Upload Section ---------------------
st.sidebar.header("Upload File")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or PPTX", type=["pdf", "pptx"])
text_chunks = None

if uploaded_file:
    st.sidebar.success("File selected...")
    if uploaded_file.name.endswith(".pdf"):
        extracted_text = extract_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(".pptx"):
        extracted_text = extract_ppt_text(uploaded_file)
    else:
        st.sidebar.error("Unsupported file type.")
        st.stop()
    text_chunks = split_text(extracted_text)

# -------------------- LangChain Tools ---------------------

@tool
def summarize_text(text=text_chunks):
    """Summarizes educational content."""
    summary.top_interface()
    return "✅ Task completed!"

@tool
def generate_questions(text=text_chunks):
    """Generates questions from educational content."""
    
    return gen_qs.sidebar_generate_questions(text)

@tool
def ask_qa(text=text_chunks)-> str:
    """Answers questions based on content."""
    ques.face(text)
    return "✅ Task completed!"

@tool
def test_knowledge(text=text_chunks):
    """Starts a quiz based on the file content."""
    quiz.start_point(text)
    return "✅ Task completed!"

@tool
def map_resources():
    """Provides nearby educational resources."""
    map_data.main_int()
    return "✅ Task completed!"


tools = [
    Tool.from_function(
        func=summarize_text,
        name="Summarizer",
        description="Use this tool to summarize educational content from PDF or PPT files."
    ),
    Tool.from_function(
        func=generate_questions,
        name="QuestionGenerator",
        description="Use this tool to generate questions from educational material."
    ),
    Tool.from_function(
        func=ask_qa,
        name="QuestionAnswering",
        description="Use this tool to answer questions based on educational documents."
    ),
    Tool.from_function(
        func=test_knowledge,
        name="KnowledgeTester",
        description="Use this tool to test user knowledge using quizzes based on content."
    ),
    Tool.from_function(
        func=map_resources,
        name="EduResourceMapper",
        description="Use this tool to suggest nearby educational centers, libraries, or resources."
    )
]



# -------------------- LangChain Agent with Gemini ---------------------
@st.cache_resource
def load_agent():
    gemini_llm = model_.load_model()
    agent = initialize_agent(
        tools=tools,
        llm=gemini_llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent

agent = load_agent()

# -------------------- User Input + AI Agent ---------------------
user_prompt=None
with st.sidebar:
    user_prompt = st.text_input("🎙️ What do you want to do? (e.g., Summarize, Create quiz, Ask questions...)")

    if user_prompt:
        if text_chunks:
            combined_text = " ".join(text_chunks[:3])
            agent_input = f"""{user_prompt}\n\nHere's the file content:\n{combined_text}
                            return it as in the following structure but in indented formatted lines not in  just the schema is given to follow the structre
                            {prompts.mcq_prompt}
                            {prompts.tf_prompt}
                            {prompts.one_liner_prompt}
                            {prompts.sum_prompt}
                            """
        else:
            agent_input = user_prompt

if user_prompt:
    #with st.sidebar:
        with st.spinner("🤖 AI Agent thinking..."):
                try:
                    result = agent.run(agent_input)
                    print(result)
                    #st.success("✅ Task completed!")
                    st.write(result)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
