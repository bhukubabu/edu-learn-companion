import random
import json
import time
import pandas as pd
from PyPDF2 import PdfReader
import streamlit as st

#------------------- Page configuration ------------------------#
st.set_page_config(
    page_icon="",
    page_title="Study Booster",
    layout="centered",
    initial_sidebar_state="expanded"
)
text_chunks=None

import ques 
import gen_qs
import summary 
#from pptx import Presentation
import map_data
from create_pdf import extract_pdf_text,extract_ppt_text,split_text


# ------------------------------ Sidebar for file upload and task selection --------------------------------#
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 750px !important;
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


menu_options=st.sidebar.radio("Choose task",options=['Edu-resource','Magic Summarizer','Ask Questions','Generate Questions'],horizontal=True)
if menu_options=="Generate Questions":
    gen_qs.sidebar_generate_questions(text_chunks)
elif menu_options=="Magic Summarizer":
    if st.sidebar.button("Generate more ✨"):
        st.rerun()
    summary.top_interface()
    st.sidebar.warning("You can either select file or type or speak ")
elif menu_options=="Ask Questions":
    ques.face(text_chunks)
elif menu_options=="Edu-resource":
    map_data.main_int()
     
