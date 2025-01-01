import folium
import random
import requests

YANDEX_GEOCODE_API_KEY = "0d997e8f-b415-4fd0-91b1-c9547916c893"

# Список городов для игры
city_list = ["Гай","Екатеринбург", "Новосибирск", "Нижний Новгород", "Москва"]

def get_coordinates(city_name):
    """Получает координаты города через геокодер."""
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    geocode_params = {
        "geocode": city_name,
        "format": "json",
        "apikey": YANDEX_GEOCODE_API_KEY
    }
    response = requests.get(geocode_url, params=geocode_params).json()
    
    try:
        position = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        coords = tuple(map(float, position.split()))
        return coords
    except (KeyError, IndexError):
        print(f"Не удалось получить координаты для города {city_name}")
        return None

def create_map_with_marker(coords, city_name, filename="city_map.html"):
    """Создает карту с маркером для указанного города."""
    city_map = folium.Map(location=[coords[1], coords[0]], zoom_start=12)  # Обратите внимание на порядок координат

    # Добавляем маркер с названием города
    folium.Marker(location=[coords[1], coords[0]], popup=city_name).add_to(city_map)

    # Сохраняем карту в файл
    city_map.save(filename)
    print(f"Карта города '{city_name}' сохранена в файл {filename}")

def play_guess_the_city():
    """Игра 'Угадай город'."""
    random.shuffle(city_list)  # Перемешиваем список городов

    for city in city_list:
        print("Показывается карта города. Угадай город!")

        # Получаем координаты города
        coords = get_coordinates(city)
        if not coords:
            continue

        # Создаем карту города с маркером
        create_map_with_marker(coords, city, f"{city}_map.html")

        # Подождем немного перед отображением следующего города
        input("Нажмите Enter, чтобы увидеть следующий город...")

        # Угадываем город
        user_guess = input("Введите ваш ответ: ").strip()
        if user_guess.lower() == city.lower():
            print("Правильный ответ!")
        else:
            print(f"Неправильно! Это был {city}.")

# Запуск игры
play_guess_the_city()
