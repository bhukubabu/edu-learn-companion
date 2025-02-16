import json
import re
import pyttsx3
import threading
import streamlit as st
import speech_recognition as sr
from model_ import load_model
from audio_recorder_streamlit import audio_recorder
#from main import text_chunks

@st.cache_data
def load_llm_model():
    return load_model()

llm_model=load_llm_model()

def output_interface(base_text,text):
    with st.spinner(text="running"):
        response_to_question=response(text=base_text, question_= text)
    #thread=threading.Thread(target=voice_response,args=(response_to_question,))
    #thread.start()
    for j,i in enumerate(response_to_question):
        with st.chat_message('assistant'):
            st.warning(f"**{i['question']}**")
        with st.expander("Show Answer "):
            st.success(f"**Answer :** {i['answer']}",icon="✅")
    st.markdown("Please tell me whether you need further assistance.I am pleased to help you.")


def voice_response(content: str):
    engine=pyttsx3.init()
    engine.say(content)
    engine.runAndWait()


def voice_input(base_text):
    recognizer = sr.Recognizer()
    try:
        # Record audio
        audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
        data=st.audio(audio_bytes,format="audio/wav")
        # Check if audio_bytes is valid
        if not audio_bytes:
            st.error("No audio detected, please try again.")
            return
        
        with st.spinner("⏳ Processing your voice input..."):
            text = recognizer.recognize_google(audio_bytes)
        
        if "thank you" in text:
            pass
        else:
            output_interface(base_text, text)
    
    except sr.UnknownValueError:
        st.error("Sorry 😩 could not understand properly")
    except sr.RequestError:
        st.error("Sorry 😩 could not understand properly")
    except ValueError as e:
        st.error(f"Error with audio data: {e}")



def response(text,question_):
    global llm_model
    prompt=f"""
    You are an help-ful assistant , you will answer to {question_} 
    based on the given context. your answer should be creative but to the point and precise. If the 
    question asked by the user is not inside the context provided to you answer from your own knowledge base
    The context is as follows :  {text}
    Use this json schema to return the response:
    [
        {{
            "question": "the given question",
            "answer":"your sample answer here",
        }}
        ...
    ]
    Each response should be returned in the mentioned schema
    """
    response=llm_model.invoke(prompt)
    json_match=re.search(r'\[.*\]',response,re.DOTALL)
    if json_match:
        json_str=json_match.group(0)
        try:
            extracted=json.loads(json_str)
            #print(extracted[0]['answer'])
            return extracted
        except:
            return "na"
    

#if __name__ == "__main__":
def face(base_text):
    st.title("Raise your queries 🗣 - I will find answer on your behalf")
    with st.chat_message('assistant'):
        st.warning("Your edu-learn companion is at your service. Tell me how can I help you today")
    
    if base_text==None:
        st.sidebar.error("No file selected")
    else:
        st.sidebar.success("Knowledge base created")
    
    with st.container(height=200):
        data=st.text_area("your question here")
    ans=st.button("Generate answer ")
    if ans:
        #voice_input(base_text)
        if data!="":
            output_interface(base_text, data)
        else:
            st.error("please enter text")
        
        
    #response(text=text_chunks, question_="What are the five components of a data communication system? answer in single line")
    #response(text=text_chunks, question_="answer the previous question in descriptive way")
