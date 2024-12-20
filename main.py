import random
import json
import pandas as pd
import time
import streamlit as st
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PyPDF2 import PdfReader
from fpdf import FPDF
from summary import top_interface
#from pptx import Presentation
from ques_ans import sidebar_generate_questions
from create_pdf import extract_pdf_text,split_text




# Function to extract text from PDF

def export_to_pdf(questions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="MCQ/TF Quiz Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    for idx, question in enumerate(questions):
            question_text = question['question']
            correct_answer = question['correct_answer']
            user_response = st.session_state.responses.get(f"question_{idx}", "No response")

            # Add question and user response
            pdf.multi_cell(0, 10, txt=f"Q{idx + 1}: {question_text}")
            pdf.cell(0, 10, txt=f"Your Answer: {user_response}", ln=True)
            pdf.cell(0, 10, txt=f"Correct Answer: {correct_answer}", ln=True)
            pdf.cell(0, 10, ln=True)  # Add some spacing

        # Save the PDF to a file
    pdf_output_path = "quiz_report.pdf"
    pdf.output(pdf_output_path)

        # Provide a download link in Streamlit
    with open(pdf_output_path, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name=pdf_output_path,
                mime="application/pdf",
            )


# Function to generate questions using the model
def update_user_input(qa_index):
    question=st.session_state.questions[qa_index]
    answer=st.session_state[f"ans_{qa_index}"]
    st.session_state.answers[f"ans_{qa_index}"]=answer.split(')')[0]


def generate_mcq_tf_(question):
    if "answers" not in st.session_state:
        st.session_state.answers={f"ans_{j}":None for j in range(len(question))}
        st.session_state.buttons={f"but_{j}": None for j in range(len(question))}

    for j,i in enumerate(question):
        st.write(f"**{i['question']}**")
        user_options=st.radio(
                "Choose the appropiate option",
                options = [f"{key}) {val}" for key,val in i['options'].items()],
                key=f"ans_{j}",
                on_change=lambda j=j:update_user_input(j)
                )
        if st.button("Show answer",key=f"but_{j}"):
            st.session_state.buttons=True

        if st.session_state.buttons[f"but_{j}"]:
            st.success(f"**Answer :** {i['correct_answer']}",icon="✅")
            selected_option=st.session_state.answers[f"ans_{j}"]

            if selected_option!=i['correct_answer']:
                st.error(f"Your answer is {user_options}",icon="❌")
            else:
                st.success(f"Your answer is {selected_option}",icon="✅")
                st.balloons()



#st.title("📚 Smart Edu-Learn Companion - ")

# Sidebar for file upload and difficulty selection
text_chunks=None
st.sidebar.header("Upload File")
uploaded_file = st.sidebar.file_uploader("Upload a PDF or PPTX", type=["pdf", "pptx"])

if uploaded_file:
    st.sidebar.success("File selected...")
    # Extract text based on file type
    if uploaded_file.name.endswith(".pdf"):
        extracted_text = extract_pdf_text(uploaded_file)
    elif uploaded_file.name.endswith(".pptx"):
        pass
        #extracted_text = extract_ppt_text(uploaded_file)
    else:
        st.sidebar.error("Unsupported file type.")
        st.stop()
    text_chunks=split_text(extracted_text)
else:
    text_chunks=None


menu_options=st.sidebar.radio("Choose task",options=['Magic Summerizer','Ask Questions','Generate Questions'],horizontal=True)


if menu_options=="Generate Questions":
    sidebar_generate_questions(text_chunks)
elif menu_options=="Magic Summerizer":
    if st.sidebar.button("Generate more ✨"):
        st.rerun()
    top_interface()
elif menu_options=="Ask Questions":
    pass
    
    



