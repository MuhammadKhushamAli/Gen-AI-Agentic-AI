from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

SYSTEM = """
You are an AI Assistant who can solve only math related problems.
You work on START, PLAN and OUTPUT steps.
You need to plan first on user input then give output.
PLAN can be multiple steps.
Once you thonk enough PLAN has been done, then you give OUTPUT.

Rules:
- Strictly follow the given JSON output format
- Only run one step at a time.
- Run the steps in the following order: START - User Input then PLAN - (can be multiple times) finally OUTPUT - (final answer given to user)

Output JSON format:
{"step": "START" | "PLAN" | "OUTPUT", content: "string"}

Examples:
START: Hey sole this 3 + 4 - 5 + 6 / 2 * 4 - 1
PLAN: {"step": "PLAN", "content": "Seems interesting, It looks like a maths problem."}
PLAN: {"step": "PLAN", "content": "I think BODMAS can solve it."}
PLAN: {"step": "PLAN", "content": "According to BODMAS first we perform the division."}
PLAN: {"step": "PLAN", "content": "Division 6 / 2 now it becomes 3 + 4 - 5 + 3 * 4 - 1"}
PLAN: {"step": "PLAN", "content": "Then multiply 3 * 4 then it becomes 3 + 4 - 5 + 12 - 1"}
PLAN: {"step": "PLAN", "content": "Then add 3 + 4 and 5 + 12 it becomes 7 - 17 - 1"}
PLAN: {"step": "PLAN", "content": "Now subtract 7 - 17 = -10 then -10 - 1 = -11"}
PLAN: {"step": "PLAN", "content": "The answer is -11, looking backward in the working to ensure that there is no mistake"}
OUTPUT: {"step": "OUTPUT", "content":"Answer is -11"}
"""

client = OpenAI()

SYSTEM_PROMPTS = [
    {"role":"system", "content": SYSTEM},
]
input = input("👍 What you want to ask: ")
SYSTEM_PROMPTS.append({"role":"user", "content": input})

while True:
    response = client.chat.completions.create(
        model = "gpt-4o",
        response_format={"type": "json_object"},
        messages = SYSTEM_PROMPTS
    )
    result = response.choices[0].message.content
    SYSTEM_PROMPTS.append({"role":"assistant", "content":result})
    result = json.loads(result)

    if result["step"] == "START":
        print(f"😂 Hmm, User ask this:\n {result.get("content")}")
    elif result["step"] == "PLAN":
        print(f"😎 Planning:\n {result.get("content")}")
    elif result["step"] == "OUTPUT":
        print(f"👌 The output is: \n {result.get("content")}")
        break