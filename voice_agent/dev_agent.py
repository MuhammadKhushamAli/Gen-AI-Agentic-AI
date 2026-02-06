from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI
import speech_recognition as sr
import asyncio
import shutil

BASE_DIR = Path("workspace")
BASE_DIR.mkdir(exist_ok=True)

def create_dir(**namedArgs):
    try:
        path = BASE_DIR / namedArgs["name"]
        path.mkdir(parents=True)
        return f"{namedArgs["name"]} is created at: {path}"
    except Exception as e:
        return e

def delete_dir(**namedArgs):
    try:
        path = BASE_DIR / namedArgs["name"]
        if path.exists() and path.is_dir():
            shutil.rmtree(path=path)
            return f"{namedArgs["name"]} successfully deleted"
        return "File not Found"
    except Exception as e:
        return e

def create_file(**namedArgs):
    try:
        path = BASE_DIR / namedArgs["name"]
        if path.exists():
            return "File already exists"
        path.write_text(namedArgs.get("content", ""))
        return f"{namedArgs["name"]} file created"
    except Exception as e:
        return e

def write_file(**named_args):
    try:
        path = BASE_DIR / named_args["name"]
        if path.exists() and path.is_file():
            path.write_text(named_args["content"])
            return f"{named_args['name']} file updated"
        return "File not found"
    except Exception as e:
        return e
    
def delete_file(**namedArgs):
    try:
        path = BASE_DIR / namedArgs["name"]
        if path.exists():
            path.unlink()
            return f"{namedArgs["name"]} file deleted"
        return "File not found"
    except Exception as e:
        return e

def load_list_of_files(**namedArgs):
    path = BASE_DIR / namedArgs["name"]
    if path.exists() and path.is_dir():
        return [f.name for f in path.iterdir()]
    return "Path not Found"

def is_exist(**namedArgs):
    path = BASE_DIR / namedArgs["name"]
    if path.exists():
        return True
    return False

load_dotenv()
async_client = AsyncOpenAI()
async def tts(speach: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in cheerfull and delight tone",
        input=speach,
        response_format="pcm"
    )as response:
        await LocalAudioPlayer().play(response)

def get_weather(**namedArgs):
    url = f"https://api.weatherapi.com/v1/current.json?key=585a954f44c84d7e90e150134262901&q={namedArgs["city"].lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        weather_data = response["current"]
        return f"{response['location']['name']} has current temperature {weather_data['temp_c']} C and feels like {weather_data['feelslike_c']} C and {weather_data['cloud']}% cloudy and humidity is {weather_data['humidity']}"
    return "Unable to fetch weather data"

tools = {
    "get_weather": get_weather,
    "create_dir": create_dir,
    "delete_dir": delete_dir,
    "create_file": create_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "load_list_of_files": load_list_of_files,
    "is_exist": is_exist
}

SYSTEM = """
- You are a voice agent you are given a transcript of what user is saying.
- Your task is to output like that you response is later converted to speach using AI and play back to user
- You have work on START (user input), PLAN (may be multiple times), TOOL (may be ones or may be multiple time depends on how many times tools are used), OBSERVE (ones after every tool call to analyse the output given by tool) and OUTPUT (ones if all the things are completed) steps

Rules:
- Output must be in JSON formate
- Only run one step at a time
- Start will START then PLAN then TOOL then OBSERVE then PLAN then OUTPUT

Output JSON formate:
{"step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT", "content": "string", "tool": "string", "input": "string", "output": "string"}

Tools:
- get_weather(city_name: string) - it takes city name as a string and gives output of weather condition in string.
- create_dir(name: string) - it create directory in BASE_DIR and take the name of dir as a string and return the success or failure result.
- delete_dir(name: string) - it delete directory in BASE_DIR and take the name of dir as a string and return the success or failure result.
- create_file(name: string, content: optional(string)) - it create file in directory you want just pass directory/name  or just file name if it is in base dir in the name parameter and return the success or failure result.
- write_file(name: string, content: string): it write to the file in directory you want just pass directory/name or just file name if it is in base dir in the name parameter and take the content of file as a string add content in the content argumenent it takes the named parameters(kwargs) like in name= name or path of directory and in content=content of file and return the success or failure result.
delete_file(name: string): it delete to the file in directory you want just pass directory/name or just file name if it is in base dir in the name parameter and return the success or failure result. - load_list_of_files(path: string): it takes the path of the directory to enlist the fies and dirs in that dir by default it is base dir
- is_exist(name:string) - it takes the path or name(if in BASE_DIR) of file or directory and retrun tru of exists adn false if not exists

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
PLAN: {"step": "TOOL", "tool": "get_weather", "input": {"city": "faisalabad"}}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": {"city": "faisalabad"}, "output": "The Temperature of the Faislabad is 10C and cloudy"}
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
PLAN: {"step": "TOOL", "tool": "get_weather", "input": {"city":"london"}}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": {"city":"london"}, "output": "The weather of London rainy and at 15C"}
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
PLAN: {"step": "TOOL", "tool": "get_weather", "input": {"city":"lahore"}}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "input": {"city":"lahore"}, "output": "The wether of Lahore is sunny at 28c"}
PLAN: {"step": "PLAN", "content": "Planning the good looking answer for you"}
OUTPUT: {"step": "OUTPUT", "content": "The weather of Lahore is sunny and the temperature there is 28 C"}

"""

class ToolInput(BaseModel):
    name: Optional[str] = Field(None, description="name of the directory or path of the directory")
    content: Optional[str] = Field(None, description="Content you want to write")
    city: Optional[str] = Field(None, description="name of city you want to check weather")
    
class MyOutputFormate(BaseModel):
    step: str = Field(..., description="It is the step LLM should take like START, PLAN, OBSERVE, OUTPUT")
    content: Optional[str] = Field(None, description="The content LLM generate in each step")
    input: Optional[ToolInput] = Field(None, description="The input parameter LLM pass to tool")
    tool: Optional[str] = Field(None, description="The tool which the generates output")

messages_arr = [
    {
        "role": "system",
        "content": SYSTEM
    }
]

client = OpenAI()
recognizer = sr.Recognizer()



print("🤖 Welcome to Agent's Office")
with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic)
    recognizer.pause_threshold = 2

    while True:
        print("🎙️: ")
        audio = recognizer.listen(mic)

        print("🔃")
        user_input = recognizer.recognize_google(audio)

        messages_arr.append({
            "role": "user",
            "content": user_input
        })

        while True:
            response =  client.chat.completions.parse(
                model="gpt-4o",
                response_format=MyOutputFormate,
                messages=messages_arr
            )
            result_raw = response.choices[0].message.content
            messages_arr.append({"role": "assistant", "content": result_raw})
            result  = response.choices[0].message.parsed
            if result.step == "START":
                print(f"\n ⭐ {result.content}")
            elif result.step == "PLAN":
                print(f"\n 📄 {result.content}")
            elif result.step == "TOOL":
                tool = result.tool
                user_input = dict(result.input)
                output = tools[tool](**user_input)
                print(f"\n 🔪Called {tool} with {user_input}🔨")
                messages_arr.append({"role": "developer", "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool,
                    "input": user_input,
                    "output": output
                })})
            elif result.step == "OUTPUT":
                asyncio.run(tts(speach=result.content))
                break


