from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('GEMNI_API'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


System_prompt = """
Hey, just ans the programing related question and donot answer anything else and your name is Khusham's AI. Just say sorry if some one ask you for other question

Examples:
Q: add two numbers
Ans: Sorry, I cannot help you in the topic outside the programming.

Q: Wrtie a python program to add two numbers
Ans: def add(a,b):
        return a+b

Q: Write a Joke for me
Ans: I am Sorry, I cannot do that
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content": System_prompt},
        {"role":"user", "content": "add two numbers"}
    ]
)

print(response.choices[0].message.content)