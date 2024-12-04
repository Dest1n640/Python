import requests
import json 
import os
API_key = 'xgSTNytyhM05oW3puNfUzIO69cA6BLfOHKoXiujK'
date = input("Укажите дату снимка(YYYY-MM-DD): ")
url = "https://api.nasa.gov/planetary/apod"
params = {"api_key":API_key, "date":date}
img = ''

response = requests.get(url, params)

if response.status_code == 200:
    js = response.json()
    img = js['url']
    
    filename = os.path.basename(img)
    download = requests.get(img)
    download.raise_for_status()
    
    if  download.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(download.content)
        print(f"Файл {filename} был успешно загружен") 
        print(f"Ссылка на изображение - {img}")
    else:
        print("Возникла ошибка при загрузке картинки")
        print(f"Ссылка на изображение - {img}")
else:
    print("Error")
    
