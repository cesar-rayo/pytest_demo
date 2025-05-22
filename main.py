import logging
import requests
import sqlite3


def is_prime(n):
    logging.debug(f"Evaluating {n}")
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        logging.debug(f"{n} % {i} = {n % i}")
        if n % i == 0:
            return False
    return True


def get_weather(city):
    response = requests.get(f"https://api.weather.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not fetch weather data")


def save_user(name, age):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUE (?, ¿)", (name, age))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print(is_prime(1))
    print(is_prime(5))
    print(is_prime(8))
    print(is_prime(33))
