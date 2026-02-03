from dotenv import load_dotenv
from mem0 import Memory
import os
import json
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1"
        }
    }
}

memory_client = Memory.from_config(config)

while True:
    user_query = input("👉 ")

    search_results = memory_client.search(query=user_query, user_id="khusham")
    
    memories = [
        f"{memory.get("id")}\nMemory:{memory.get("memory")}\n\n"
        for memory in search_results.get("results")
    ]

    SYSTEM = f"""
    Here is the User's Context:
    {json.dumps(memories)}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_query}
        ]
    )

    llm_response = response.choices[0].message.content

    print(f"🤖-> {llm_response}")

    res = memory_client.add(
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": llm_response}
        ],
        user_id="khusham"
    )