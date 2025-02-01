import requests
import json 
country = input("Введите город в которой хотите узнать погоду(На русском с большой буквы): ")
api_key = "b4c81981362fb8a448111dc385aca644"
url = "https://api.openweathermap.org/data/2.5/weather"
params={"lang":"ru", "units":"metric", "q":country, "appid":api_key}

#response = requests.get("https://api.openweathermap.org/data/2.5/weather?q={country}&appid={b4c81981362fb8a448111dc385aca644}&units{'metric'}&lang{'ru'}")
response = requests.get(url, params)
if response.status_code == 200:
    js = response.json()
    weather = js['weather'][0]['description']
    deg = js['main']["temp"] 
    wind = js["wind"]["speed"]
    humidity =  js["main"]["humidity"]
    feel = js["main"]["feels_like"]
    print(f"На данный момент в городе {country} - {weather}, температура: {deg}°C, но будет ощущаться на: {feel}°C. Ветер достигнет скорости {wind}м/c. Количество осадков - {humidity}%")
else:
    print("Error")