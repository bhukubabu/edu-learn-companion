import json
import re
import pyttsx3
import threading
import streamlit as st
import speech_recognition as sr
from model_ import load_model
#from main import text_chunks

@st.cache_data
def load_llm_model():
    return load_model()

llm_model=load_llm_model()

def output_interface(base_text,text):
    response_to_question=response(text=base_text, question_= text)
    thread=threading.Thread(target=voice_response,args=(response_to_question,))
    thread.start()
    with st.chat_message('assistant'):
        st.success(response_to_question)
    st.markdown("Please tell me whether you need further assistance.I am pleased to help you.")


def voice_response(content: str):
    engine=pyttsx3.init()
    engine.say(content)
    engine.runAndWait()


def voice_input(base_text):
    recognizer=sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
            #st.markdown("Listening....")
        while True:
            try:
                audio=recognizer.listen(source,timeout=10)
                with st.spinner("⏳ Processing your voice input..."):
                    text=recognizer.recognize_google(audio)
                if "thank you" in text:
                    break
                else:
                    output_interface(base_text, text)
                
            except sr.UnknownValueError:
                st.error("Sorry 😩 could not understand properly")
                #return None
            except sr.RequestError:
                st.error("Sorry 😩 could not understand properly")
                #return None

def response(text,question_):
    global llm_model
    prompt=f"""
    You are an help-ful assistant , you will answer to the questions asked by the user 
    based on the given context. your answer should be creative but to the point. If the 
    question asked by the user is not inside the context provided to you answer from your own knowledge base
    The context is as follows :  {text}
    Use this json schema to return the response:
    [
        {{
            "question": "{question_}",
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
            print(extracted[0]['answer'])
            return extracted[0]['answer']
        except:
            return "na"
    

#if __name__ == "__main__":
def face(base_text):
    st.title("Raise your queries 🗣 - I will find answer on your behalf")
    with st.chat_message('assistant'):
        st.warning("Your edu-learn companion is at your service. Tell me how can I help you today")
    speak=st.button("Speak 🔊")
    if base_text==None:
        st.sidebar.error("No file selected")
    else:
        st.sidebar.success("Knowledge base created")
    
    if speak:
        voice_input(base_text)
        
        
    #response(text=text_chunks, question_="What are the five components of a data communication system? answer in single line")
    #response(text=text_chunks, question_="answer the previous question in descriptive way")