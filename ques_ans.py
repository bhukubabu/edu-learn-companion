import time
import streamlit as st
from model_ import generate_response


def generate_mcq_tf(question):
     for j,i in enumerate(question):
        st.warning(f"**Q{j+1}. {i['question']}**")
        for key,val in i['options'].items():
            st.markdown(f"{key}) {val}")
        st.success(f"**Answer :** {i['correct_answer']}",icon="✅")


def gen_question_interface(text_chunks,difficulty,question_type):

    st.title("📚 Smart Edu-Learn Companion - Automated Quiz Generator")
    questions_data = []
    
    for i, chunk in enumerate(text_chunks[:5]):  # Limit to 5 chunks for demo
        generated_content= generate_response(chunk, difficulty,question_type)
        with st.spinner(f"Have paitence......\n Your 📚 Smart Edu-Learn Companion is generating best response for you"):
            time.sleep(5)
        st.subheader("Generated Quiz")
        #st.session_state.questions=generated_content
        if question_type=='MCQ (multiple choice question)' or question_type=='TRUE/FALSE':
            generate_mcq_tf(generated_content)
        
        questions_data.append(generated_content)
    #if export_quiz:
    #   export_to_pdf(generated_content)


def sidebar_generate_questions(text_chunks):
    difficulty = st.sidebar.selectbox("Select Difficulty Level", ["easy", "medium", "hard"])
    question_type=st.sidebar.selectbox("Select question type",options=['MCQ (multiple choice question)','TRUE/FALSE','Short','Descriptive'])
    col1,col2=st.sidebar.columns(2)
    
    with col1:
        gen=st.sidebar.button("Generate")
    with col2:
        export=st.sidebar.button("Export quiz")

    if gen:
        if text_chunks!=None:
            gen_question_interface(text_chunks,difficulty,question_type)
        else:
            st.sidebar.error("Please select the file")