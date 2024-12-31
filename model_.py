import os
import re
import json
from langchain_google_genai import GoogleGenerativeAI


def load_model():
    llm=GoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.environ['GEMINI_API_KEY'],
    temperature=0,
    top_k=40,
    max_output_tokens=8192,
    top_p=0.95,
    )
    return llm

def generate_prompts(text,difficulty,type_qa):
    system_prompt_start = f"""
    You are an AI assistant who will generate {difficulty} level {type_qa} type questions 
    from the given content.Ensure that questions should not repeat"""  

    mcq_schema= f"""
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
        Content :
        {text}
        """
    
    tf_prompt= f"""
        Ensure the output is a valid JSON array that matches this structure
        [
            {{
                "question": "Your question text here",
                "options": {{
                    "1": "option 1 text should be Either true or false",
                    "2": "option 1 text should be Either true or false but not same as option 1"
                }},
                "correct_answer":"Correct option label with option value"
            }}
        .....
        ] 
        Content :
        {text}
        """
    one_liner=f"""
        Ensure the output is a valid JSON array that matches this structure
        [
            {{
                "question": "Your question text here",
                "correct_answer": "sample short precise answer here"
            }}
            ....
        ]
        Content :
        {text}
        """
    des_qes= f"""
        Ensure the output is a valid JSON array that matches this structure
            {{
                "question": "Your question text here",
                "correct_answer": "sample answer here in paragraphed divided 
                    text along with bulleted points in few parts of answer"
            }}
            ....
        ] 
        Content :
        {text}
        """
    #'MCQ (multiple choice question)','TRUE/FALSE','Short','Descriptive'

    if type_qa=='MCQ (multiple choice question)':
        return system_prompt_start+mcq_schema
    elif type_qa=='TRUE/FALSE':
        return system_prompt_start+tf_prompt
    elif type_qa=='Descriptive':
        return system_prompt_start+des_qes
    else:
        return system_prompt_start+one_liner
    
def generate_response(text, difficulty="medium",type_qa='short'):
    llm_model,prompt=load_model(),generate_prompts(text,difficulty,type_qa)
    response=llm_model.invoke(prompt)
    print(response)
    json_match=re.search(r'\[.*\]',response,re.DOTALL)
    if json_match:
        json_str=json_match.group(0)
        try:
            extracted=json.loads(json_str)
            print(extracted)
            return extracted
        except:
            return "na"



text= """ChatGPT is a generative artificial intelligence chatbot developed by OpenAI and launched in 2022.
    It is currently based on the GPT-4o large language model. ChatGPT can generate human-like conversational
   responses and enables users to refine and steer a conversation towards a desired length, format, style,
     level of detail, and language. It is credited with accelerating the AI boom, which has led to ongoing 
     rapid investment in and public attention to the field of artificial intelligence. Some observers have 
     raised concern about the potential of ChatGPT and similar programs to displace human intelligence, enable plagiarism, or fuel misinformation.
"""
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





