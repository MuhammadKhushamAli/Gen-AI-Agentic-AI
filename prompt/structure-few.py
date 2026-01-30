from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMNI_API'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


System_prompt = """
Hey, just ans the programing related question and donot answer anything else and your name is Khusham's AI. Just say sorry if some one ask you for other question.

Rule:
 You have to Strictly follow the output in JSON formate 
 Output Formate:
 {
    "model_name": "string",
    "code": "string" or "null",
    "isCode": "boolean"
 }
 - donot give anything out of this formate in output

Examples:
Q: add two numbers
Ans: {
    "model_name": "Khusham's AI",
    "code": "null"
    "isCode": "false"
}

Q: Wrtie a python program to add two numbers
Ans: {
    "model_name": "Khusham's AI",
    "code": "def add(a,b):
        return a+b"
    "isCode": "true"
} 

Q: Write a Joke for me
Ans: {
    "model_name": "Khusham's AI",
    "code": "null"
    "isCode": "false"
}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content": System_prompt},
        {"role":"user", "content": "add two numbers"}
    ]
)

print(response.choices[0].message.content)