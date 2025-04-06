import os
import re
import json
import pyttsx3
import threading
import streamlit as st
from gtts import gTTS
#from playsound import playsound
from langdetect import detect
from model_ import load_model
import speech_recognition as sr


def magic_summarizer(text,level):
    llm_model=load_model()
    prompt=f"""
    please generate {level} summary of the text given below {text} 
    and return the output in json format. Please answer in the user provided language always.
    Each response  should be returned in JSON format as given below :
    [
        {{
            "content": "the given content",
            "summary":" the sample summerize text"
        }}
        .....
    ]
    """
    response=llm_model.invoke(prompt)
    json_match=re.search(r'\[.*\]',response,re.DOTALL)
    if json_match:
        json_str=json_match.group(0)
        try:
            extracted=json.loads(json_str)
            return extracted[0]['summary']
        except:
            return "na"
    

def assistant_speak(content):
    engine=pyttsx3.init()
    engine.say(content)
    engine.runAndWait()
    playsound("audio_output.mp3")


def record():
    rec=sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown("Listening...........")
        rec.adjust_for_ambient_noise(source)
        con=rec.listen(source,timeout=10)
    try:
        text=rec.recognize_google(con)
        return text
    except sr.UnknownValueError:
        st.error("Sorry couldn't understand properly")
        return None
    except sr.RequestError:
        st.error("Could not request result")
        return None


def top_interface():
    st.title("🤖AI Summarizer ✨")
    with st.container(height=400,border=True):
        #if st.button("Speak..."):
            #recorded=record()
           # if recorded!=None:
               # st.text_area(recorded,height=250)
               # content=recorded[:]
        #else:
            content=st.text_area("Write your text here",height=250)
    try:
        lang=detect(content)
    except:
        pass
    min_val,max_val,step,cre=0,10,1,None
    level=st.slider("Choose ceativity level",min_val,max_val,step)
    if level==(min_val+max_val)/2:
        cre="medium creative"
    elif level>(min_val+max_val)/2:
        cre="highly creative"
    else:
        cre="standard"
    
    if st.button("Summarize"):
        bottom_interface(content,cre,lang)


def bottom_interface(text,creativity_level,lang="en"):
    extracted=magic_summarizer(text,creativity_level)
    audio_file=gTTS(text = extracted, lang=lang)
    audio_file_path="audio_output.mp3"
    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)
    audio_file.save(audio_file_path)
    audio_thread=threading.Thread(target=assistant_speak,args=({"Here's is your sample generated response."},))
    audio_thread.start()

    with st.chat_message("assistant"):
        st.markdown(extracted)
    audio_thread.join()
    
