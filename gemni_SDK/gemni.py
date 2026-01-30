from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMNI_API")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello I am Muhammad Khusham Ali! Do you know about me?"
)

print(response.text)