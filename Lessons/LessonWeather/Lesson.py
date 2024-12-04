import requests
import json
counrty = input()
response = requests.get("https://api.openweathermap.org/data/2.5/weather?q={country}&appid={}}&lang=ru&units=metric")
if response.status_code == 200:
    js = response.json()
    result = json.loads(js)
    print(result["weather"[0]["description"]])
