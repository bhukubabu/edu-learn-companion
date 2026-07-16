import random
import json
import time
import pandas as pd
from PyPDF2 import PdfReader
import streamlit as st

st.set_page_config(
      page_icon="",
      page_title="Study Booster",
      layout="centered",
      initial_sidebar_state="expanded"
)

import ques
import gen_qs
import summary
import map_data
from create_pdf import extract_pdf_text, extract_ppt_text, split_text

  st.markdown("""""", unsafe_allow_html=True)

  st.sidebar.header("Upload File")
  uploaded_file = st.sidebar.file_uploader("Upload a PDF or PPTX", type=["pdf", "pptx"])

  # ✅ Use session_state to persist text_chunks across reruns
  if uploaded_file:
      st.sidebar.success("File selected...")

      # Only reprocess if a new file is uploaded
      if "uploaded_file_name" not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
          if uploaded_file.name.endswith(".pdf"):
              extracted_text = extract_pdf_text(uploaded_file)
          elif uploaded_file.name.endswith(".pptx"):
              extracted_text = extract_ppt_text(uploaded_file)
          else:
              st.sidebar.error("Unsupported file type.")
              st.stop()

          st.session_state.text_chunks = split_text(extracted_text)
          st.session_state.uploaded_file_name = uploaded_file.name  # track which file is loaded

      text_chunks = st.session_state.text_chunks

  else:
      text_chunks = None
      # Clear stored chunks if file is removed
      st.session_state.pop("text_chunks", None)
      st.session_state.pop("uploaded_file_name", None)

  menu_options = st.sidebar.radio(
      "Choose task",
      options=['Edu-resource', 'Magic Summarizer', 'Ask Questions', 'Generate Questions'],
      horizontal=True
  )

if menu_options == "Generate Questions":
      gen_qs.sidebar_generate_questions(text_chunks)
elif menu_options == "Magic Summarizer":
      if st.sidebar.button("Generate more ✨"):
          st.rerun()
      summary.top_interface(text_chunks)
      st.sidebar.warning("You can either select file or type or speak")
elif menu_options == "Ask Questions":
      ques.face(text_chunks)
elif menu_options == "Edu-resource":
      map_data.main_int()
