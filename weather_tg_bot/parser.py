import datetime
import json

from aiohttp import ClientSession

from weather_tg_bot.config import config

CODE_TO_SMILE = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь 🌧",
        "Drizzle": "Дождь 🌧",
        "Thunderstorm": "Гроза ⛈",
        "Snow": "Снег ❄️",
        "Mist": "Туман 🌫",
    }


class WeatherParser:
    """Парсер погоды."""

    async def init(self) -> None:
        """Инициализация парсера."""
        self.session = ClientSession()

    async def get_weather(self, city: str) -> str:
        """Получить погоду.

        Returns:
            Погоду в указаном городе.

        """
        try:
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": config.open_weather_token,
                "units": "metric",
            }
            async with self.session.get(url, params=params) as r:
                data = json.loads(await r.text())

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            wd = CODE_TO_SMILE.get(weather_description, weather_description)

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"],
            ) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"],
            )

            return (
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"Погода в городе: {city}\n"
                f"Температура: {cur_weather}C° {wd}\n"
                f"Влажность: {humidity}%\n"
                f"Давление: {pressure} мм.рт.ст\n"
                f"Ветер: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\n"
                f"Закат солнца: {sunset_timestamp}\n"
                f"Продолжительность дня: {length_of_the_day}\n"
            )

        except Exception as e:  # noqa: BLE001
            return f"Во время работы произошла ошибка:\n\n{e}"
