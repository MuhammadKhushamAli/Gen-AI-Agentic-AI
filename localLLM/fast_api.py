from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def home():
    return {"Hello":"World"}

@app.post("/chat")
def chat(
    message: str = Body(..., description="User's Input")
):
    response = client.chat(
        model="gemma:2b",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return {"response": response.message.content}