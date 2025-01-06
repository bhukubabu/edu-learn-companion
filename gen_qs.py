import time
import streamlit as st
from model_ import generate_response


def generate_mcq_tf(question):
     for j,i in enumerate(question):
        with st.chat_message('assistant'):
            st.warning(f"**Q{j+1}. {i['question']}**")
        for key,val in i['options'].items():
            st.markdown(f"{key}) {val}")
        with st.expander("Show Answer "):
            st.success(f"**Answer :** {i['correct_answer']} {i['options'][i['correct_answer']]}",icon="✅")
     #st.rerun()
     time.sleep(1)

def generate_short_des(question):
     for j,i in enumerate(question):
        with st.chat_message('assistant'):
            st.warning(f"**Q{j+1}. {i['question']}**")
        with st.expander("Show Answer "):
            st.success(f"**Answer :** {i['correct_answer']} ",icon="✅")
     #st.rerun()
     time.sleep(1)

def sidebar_generate_questions(text_chunks):
    st.title("📚 Smart Edu-Learn Companion")
    #st.title("📚 Smart Edu-Learn Companion - Automated Quiz Generator")
    if "difficulty" not in st.session_state:
        st.session_state.difficulty="easy"
    if "question_type" not in st.session_state:
        st.session_state.question_type="MCQ (multiple choice question)"
    if "generated_content" not in st.session_state:
        st.session_state.generated_content=None

    difficulty = st.sidebar.selectbox("Select Difficulty Level", ["easy", "medium", "hard"])
    question_type=st.sidebar.selectbox("Select question type",options=['MCQ (multiple choice question)','TRUE/FALSE','Short','Descriptive'])
    

    if difficulty != st.session_state.difficulty:
        st.session_state.difficulty=difficulty
    if question_type!= st.session_state.question_type:
        st.session_state.question_type=question_type

    col1,col2=st.sidebar.columns(2)
    with col1:
        gen=st.sidebar.button("Generate")
    with col2:
        export=st.sidebar.button("Export quiz")

    if gen:
        if text_chunks!=None:
            with st.spinner(f"Have paitence......\n Your 📚 Smart Edu-Learn Companion is generating best response for you"):
                    generated_content=generate_response(text_chunks,difficulty,question_type)
                    st.session_state.generated_content=generated_content
            if question_type=='MCQ (multiple choice question)' or question_type=='TRUE/FALSE':
                    generate_mcq_tf(st.session_state.generated_content)
            if question_type=='Short' or question_type=='Descriptive':
                    generate_short_des(st.session_state.generated_content)
        else:
            st.sidebar.error("Please select file")
    else:
        if st.session_state.generated_content:
            generated_content=st.session_state.generated_content
            if question_type=='MCQ (multiple choice question)' or question_type=='TRUE/FALSE':
                    generate_mcq_tf(generated_content)
            elif question_type=='Short' or question_type=='Descriptive':
                     generate_short_des(generated_content)
