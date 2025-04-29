import requests
from tkinter import Tk, Button, Label, StringVar
from tkinter import ttk
from data.all_cities import get_all_cities

all_cities = get_all_cities("C:\\projects\\python\\openWeather\\data\\03_all_cities.xlsx")

def get_weather():
    city = city_combobox.get()
    key = "2c87f61e60da21c93265bb35f46b0816"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        description = weather_data["weather"][0]["description"]
        visibility = weather_data["visibility"]
        coord = [weather_data["coord"]["lon"], weather_data["coord"]["lat"]]
        info.set(f"Координаты: \nДолгота: {coord[0]}\t Широта: {coord[1]}\nТемпература: {temperature}\nОщущается как: {feels_like}\nСостояние: {description}\nВидимость: {visibility}")
    else:
        info.set(f"Ошибка: {response.status_code} - {response.text}")

root = Tk()
root.title("Прогноз погоды")
root.geometry("300x250")

city_combobox = ttk.Combobox(root, values=all_cities, font=30)
city_combobox.pack(pady=10)

btn = Button(root, text="Получить погоду", command=get_weather)
btn.pack(pady=10)

info = StringVar()
label = Label(root, textvariable=info, font=20)
label.pack(pady=20)

root.mainloop()