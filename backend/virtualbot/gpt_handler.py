# gpt_handler.py
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")       
openai.api_key = os.getenv("OPENAI_API_KEY")         
openai.api_version = "2024-02-15-preview"            

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")      

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful virtual health assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
