from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()

def get_weather(city: str):
    url = f"https://api.weatherapi.com/v1/current.json?key=585a954f44c84d7e90e150134262901&q={city.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        weather_data = response["current"]
        return f"{response["location"]["name"]} has current temperature {weather_data["temp_c"]} C and feels like {weather_data["feelslike_c"]} C and {weather_data["cloud"]}% cloudy and humidity is {weather_data["humidity"]}"
    return "Unable to fetch weather data"

tools = {
    "get_weather": get_weather
}

SYSTEM = """
- You are an AI Weather Agent you have to predict the weather
- You have work on START (user input), PLAN (may be multiple times), TOOL (may be ones or may be multiple time depends on how many times tools are used), OBSERVE (ones after every tool call to analyse the output given by tool) and OUTPUT (ones if all the things are completed) steps

Rules:
- Output must be in JSON formate
- Only run one step at a time
- Start will START then PLAN then TOOL then OBSERVE then PLAN then OUTPUT

Output JSON formate:
{"step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT", "content": "string", "tool": "string", "input": "string", "output": "string"}

Tools:
- get_weather(city_name: string) - it takes city name as a string and gives output of weather condition in string

Example 1:
START: What is the weather in Faisalabad?
PLAN: {"step": "PLAN", "content": "Nice, it seems that you are interested in the weather condition of Faisalabad"}
PLAN: {"step": "PLAN", "content": "Looking for country where is Faisalabad situated"}
PLAN: {"step": "PLAN", "content": "Wow, it is interesting it is in Pakistan which is in Asia"}
PLAN: {"step": "PLAN", "content": "Looking towards Province of Faisalabad in Pakistan"}
PLAN: {"step": "PLAN", "content": "Hmm, nice it is in Punjab"}
PLAN: {"step": "PLAN", "content": "Punjab is the Urban Province"}
PLAN: {"step": "PLAN", "content": "Now, looking for the geographical location of Faisalabad"}
PLAN: {"step": "PLAN", "content": "Seems more interesting, it is in northeast reigon of Punjab"}
PLAN: {"step": "TOOL", "tool": "get_weather", "input": "faisalabad"}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": "faisalabad", "output": "The Temperature of the Faislabad is 10C and cloudy"}
PLAN: {"step": "PLAN", "content": "Planning the good looking answer for you"}
OUTPUT: {"step": "OUTPUT", "content": "The weather of Faisalabad is cloudy and the temperature there is 10 C}

Example 2:
START: What is the weather in London?
PLAN: {"step": "PLAN", "content": "Nice, it seems that you are interested in the weather condition of London"}
PLAN: {"step": "PLAN", "content": "Looking for country where is London situated"}
PLAN: {"step": "PLAN", "content": "London is located in the United Kingdom which is in Europe"}
PLAN: {"step": "PLAN", "content": "Finding the region of London in the United Kingdom"}
PLAN: {"step": "PLAN", "content": "London is located in England"}
PLAN: {"step": "PLAN", "content": "England is part of Great Britain"}
PLAN: {"step": "PLAN", "content": "Now, looking for the geographical location of London"}
PLAN: {"step": "PLAN", "content": "London is located in the southeastern part of England"}
PLAN: {"step": "TOOL", "tool": "get_weather", "input": "london"}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": "london", "output": "The weather of London rainy and at 15C"}
PLAN: {"step": "PLAN", "content": "Planning the good looking answer for you"}
OUTPUT: {"step": "OUTPUT", "content": "The weather of London is rainy and the temperature there is 15 C"}


Example 3:
START: What is the weather in Lahore?
PLAN: {"step": "PLAN", "content": "Nice, it seems that you are interested in the weather condition of Lahore"}
PLAN: {"step": "PLAN", "content": "Looking for country where is Lahore situated"}
PLAN: {"step": "PLAN", "content": "Lahore is located in Pakistan which is in Asia"}
PLAN: {"step": "PLAN", "content": "Finding the province of Lahore in Pakistan"}
PLAN: {"step": "PLAN", "content": "Lahore is in Punjab province"}
PLAN: {"step": "PLAN", "content": "Punjab is one of the most populated provinces"}
PLAN: {"step": "PLAN", "content": "Now checking the geographical location of Lahore"}
PLAN: {"step": "PLAN", "content": "Lahore is located in the northeast part of Punjab"}
PLAN: {"step": "TOOL", "tool": "get_weather", "input": "lahore"}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": "lahore", "output": "The wether of Lahore is sunny at 28c"}
PLAN: {"step": "PLAN", "content": "Planning the good looking answer for you"}
OUTPUT: {"step": "OUTPUT", "content": "The weather of Lahore is sunny and the temperature there is 28 C"}

"""

messages_arr = [
    {
        "role": "system",
        "content": SYSTEM
    }
]

client = OpenAI()

print("🌧️Welcome to AI-Weather Forcating Agent's Office🌩️")

while True:
    user_input = input("🌥️Enter you desired city name for weather pridiction: ")

    messages_arr.append({
        "role": "user",
        "content": user_input
    })

    while True:
        response =  client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages_arr
        )
        result = response.choices[0].message.content
        messages_arr.append({"role": "assistant", "content": result})
        result = json.loads(result)

        if result["step"] == "START":
            print(f"\n\n ⭐ {result["content"]}")
        elif result["step"] == "PLAN":
            print(f"\n\n 📄 {result["content"]}")
        elif result["step"] == "TOOL":
            tool = result["tool"]
            user_input = result["input"]
            output = tools[tool](user_input)
            print(f"\n\n 🔪Called {tool} with {user_input}🔨")
            messages_arr.append({"role": "developer", "content": json.dumps({
                "step": "OBSERVE",
                "tool": tool,
                "input": user_input,
                "output": output
            })})
            continue
        elif result["step"] == "OUTPUT":
            print(f"\n\n 👋 {result["content"]}")
            break


