import requests

def get_weather(city: str):
    url = f"https://api.weatherapi.com/v1/current.json?key=585a954f44c84d7e90e150134262901&q={city.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        weather_data = response["current"]
        return f"{response["location"]["name"]} has current temperature {weather_data["temp_c"]} C and feels like {weather_data["feelslike_c"]} C and {weather_data["cloud"]}% cloudy and humidity is {weather_data["humidity"]}"
    return "Unable to fetch weather data"

print(get_weather("faisalabad"))