import os
import re
import json
import pyttsx3
import threading
import streamlit as st
from gtts import gTTS
from playsound import playsound
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
        if st.button("Speak..."):
            recorded=record()
            if recorded!=None:
                st.text_area(recorded,height=250)
                content=recorded[:]
        else:
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
        bottom_interface(content,lang,cre)


def bottom_interface(text,lang,creativity_level):
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


text= """ChatGPT is a generative artificial intelligence chatbot developed by OpenAI and launched in 2022.
     It is currently based on the GPT-4o large language model. ChatGPT can generate human-like conversational
     responses and enables users to refine and steer a conversation towards a desired length, format, style,
     level of detail, and language. It is credited with accelerating the AI boom, which has led to ongoing 
     rapid investment in and public attention to the field of artificial intelligence. Some observers have 
     raised concern about the potential of ChatGPT and similar programs to displace human intelligence, enable 
     plagiarism, or fuel misinformation."""

prompt_ = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) 
    based on the following text: '{text}' . Please generate difficulty level MCQs from the text. 
    Each question should be returned in JSON format as follows:

    [
        {{
            "question": "Your question text here",
            "options": {{
                "A": "Option A text",
                "B": "Option B text",
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "Correct option label (A, B, C, or D)"
        }},
        ...
    ]

    Ensure the JSON contains a list of MCQs, with each MCQ adhering to the structure above.
    """
    







