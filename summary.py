import json
import pyttsx3
import threading
import streamlit as st
from model_ import load_model
import speech_recognition as sr


def magic_summarizer(text,level):
    sum_model=load_model()
    prompt=f"""
    please generate {level} summary of the text given below {text} 
    and return the output in json format. Each response  should be 
    returned in JSON format as given below :
    [
        {{
            "content": "the given content",
            "summary":" the sample summerize text"
        }}
        .....
    ]
    """
    response=json.loads(sum_model.generate_content(prompt).text)
    return response[0]['summary']

def assistant_speak(content):
    engine=pyttsx3.init()
    engine.say(content)
    engine.runAndWait()

def record():
    rec=sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown("Listening...........")
        rec.adjust_for_ambient_noise(source)
        con=rec.listen(source)
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
    
    min_val,max_val,step,cre=0,10,1,None
    level=st.slider("Choose ceativity level",min_val,max_val,step)
    if level==(min_val+max_val)/2:
        cre="medium creative"
    elif level>(min_val+max_val)/2:
        cre="highly creative"
    else:
        cre="standard"
    
    if st.button("Summarize"):
        bottom_interface(content,cre)


def bottom_interface(text,creativity_level):
    extracted=magic_summarizer(text,creativity_level)
    audio_thread=threading.Thread(target=assistant_speak,args=(f"Here's is your sample generated response {extracted}",))
    audio_thread.start()
    with st.chat_message("assistant"):
        st.markdown(extracted)
    audio_thread.join()
    #print(extracted)

        
    

text= """ChatGPT is a generative artificial intelligence chatbot developed by OpenAI and launched in 2022.
    It is currently based on the GPT-4o large language model. ChatGPT can generate human-like conversational
   responses and enables users to refine and steer a conversation towards a desired length, format, style,
     level of detail, and language. It is credited with accelerating the AI boom, which has led to ongoing 
     rapid investment in and public attention to the field of artificial intelligence. Some observers have 
     raised concern about the potential of ChatGPT and similar programs to displace human intelligence, enable plagiarism, or fuel misinformation.
"""
#extract(text)




