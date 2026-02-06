import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from openai.helpers import LocalAudioPlayer
from openai import AsyncOpenAI
import speech_recognition as sr

load_dotenv()

async_client = AsyncOpenAI()
client = OpenAI()

async def tts(speach: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in cheerfull and delight tone",
        input=speach,
        response_format="pcm"
    )as response:
        await LocalAudioPlayer().play(response)

def main():
    SYSTEM = """
     You are a voice agent you are given a transcript of what user is saying.
     Your task is to output like that you response is later converted to speach using AI and play back to user
    """
    messages = [
        {"role": "system", "content": SYSTEM}
    ]
    recognizer = sr.Recognizer()

    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.pause_threshold = 2


        while True:
            print("Speak Something...")
            audio = recognizer.listen(mic)

            print("Recognizing Speak")
            stt = recognizer.recognize_google(audio)

            print(stt)

            
            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=messages
            )
            raw_response = response.choices[0].message.content
            messages.append({"role":"assistant", "content":raw_response})
            asyncio.run(tts(speach=raw_response))


main()