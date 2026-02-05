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
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "adminKhusham"
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

    get_all_results = memory_client.get_all(user_id="khusham")
    print(f"All Results: {json.dumps(get_all_results, indent=4)}")

    user_query = input("👉 ")

    search_results = memory_client.search(query=user_query, user_id="khusham")

    print(f"\n\n\nResults: {json.dumps(search_results, indent=4)}")
    
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