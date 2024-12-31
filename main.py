import random
import json
import time
import pandas as pd
from PyPDF2 import PdfReader
from fpdf import FPDF
import streamlit as st

#------------------- Page configuration ------------------------#
st.set_page_config(
    page_icon="",
    page_title="Study Booster",
    layout="centered",
    initial_sidebar_state="expanded"
)
text_chunks=None

from ques import face
from summary import top_interface
#from pptx import Presentation
from gen_qs import sidebar_generate_questions
from create_pdf import extract_pdf_text,extract_ppt_text,split_text


# ------------------------------ Sidebar for file upload and task selection --------------------------------#
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 550px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------ Sidebar for file upload and task selection --------------------------------#

st.sidebar.header("Upload File")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or PPTX", type=["pdf", "pptx"])
if uploaded_file:
    st.sidebar.success("File selected...")
    # Extract text based on file type
    if uploaded_file.name.endswith(".pdf"):
        extracted_text = extract_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(".pptx"):
        extracted_text = extract_ppt_text(uploaded_file)
    else:
        st.sidebar.error("Unsupported file type.")
        st.stop()
    text_chunks=split_text(extracted_text)
else:
    text_chunks=None


menu_options=st.sidebar.radio("Choose task",options=['Magic Summarizer','Ask Questions','Generate Questions'],horizontal=True)
if menu_options=="Generate Questions":
        sidebar_generate_questions(text_chunks)
elif menu_options=="Magic Summarizer":
    if st.sidebar.button("Generate more ✨"):
        st.rerun()
    top_interface()
    st.sidebar.warning("You can either select file or type or speak ")
    
        
elif menu_options=="Ask Questions":
        face(text_chunks)
        
    
    



