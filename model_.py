import json
import google.generativeai  as genai


def load_model():
    genai.configure(api_key="AIzaSyAbLRF9lARj4axLG1IWWoDiZydK_GNLbLg")
    generation_config={
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }

    model=genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config
    )
    return model


def varrient_prompt(qs_type):
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
                "correct_answer": "Correct option label (A, B, C, or D) with the text for label (A, B, C, or D)"
            }},
            ...
        ] """
    
    tf_prompt= f"""
        Each question should be returned in JSON format as follows:
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
        ] """
    one_liner=f"""
        Each question should be returned in JSON format as follows:
        [
            {{
                "question": "Your question text here",
                "correct_answer": "sample short precise answer here"
            }}
            ....
        ]
        """
    des_qes= f"""
        Each question should be returned in JSON format as follows:
        [
            {{
                "question": "Your question text here",
                "correct_answer": "sample answer here in paragraphed divided 
                    text along with bulleted points in few parts of answer"
            }}
            ....
        ] """
    #'MCQ (multiple choice question)','TRUE/FALSE','Short','Descriptive'

    if qs_type=='MCQ (multiple choice question)':
        return mcq_schema
    elif qs_type=='TRUE/FALSE':
        return tf_prompt
    elif qs_type=='Descriptive':
        return des_qes
    else:
        return one_liner

def generate_prompts(text, difficulty,type_qa):

    system_prompt_start = f"""
    You are an AI assistant helping the user generate {type_qa} type  questions
    based on the following text: '{text}' . Please generate {difficulty} level from the text. Each time you will
    generate different questions same questions should not repeat""" 

    system_prompt_end=f"""
         Ensure the JSON contains a list of {type_qa} with each {type_qa} adhering to the structure above.
    """
    schema=varrient_prompt(type_qa)

    main_prompt=system_prompt_start + schema + system_prompt_end

    return main_prompt
    
def generate_response(text, difficulty="medium",type_qa='short'):
    mod=load_model()
    prompt=generate_prompts(text,difficulty,type_qa)
    response=mod.generate_content(prompt).text
    extracted=json.loads(response)
    return extracted



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



def demo():
    extracted=generate_response(text,"easy",'MCQ (multiple choice question)')

    for i in range(len(extracted)):
        print(f"{i+1}. {extracted[i]['question']}")
        print("** Options **")
        for value in extracted[i]['options']:
            #print('--'*5)
            print(f" {value}. {extracted[i]['options'][value]}")
            #print('--'*5)
        print()
        ans=extracted[i]['correct_answer']
        print(f"✅ correct answer : {ans}) {extracted[i]['options'][ans]} ")
        print(" * "*10)
        if(input("want to continue? [Y/N]").lower()=='y'):
            continue
        else:
            print("HAVE A NICE DAY. ☺️")
            break




