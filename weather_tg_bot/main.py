import datetime

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from weather_tg_bot.config import config

dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message) -> None:
    await message.answer("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message()
async def get_weather(message: types.Message) -> None:
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={config.open_weather_token}&units=metric",
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

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

        await message.answer(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Погода в городе: {city}\n"
            f"Температура: {cur_weather}C° {wd}\n"
            f"Влажность: {humidity}%\n"
            f"Давление: {pressure} мм.рт.ст\n"
            f"Ветер: {wind} м/с\n"
            f"Восход солнца: {sunrise_timestamp}\n"
            f"Закат солнца: {sunset_timestamp}\n"
            f"Продолжительность дня: {length_of_the_day}\n",
        )

    except:  # noqa: E722
        await message.answer("\U00002620 Проверьте название города \U00002620")


async def main() -> None:
    """Запуск бота."""
    bot = Bot(token=config.tg_bot_token)
    await dp.start_polling(bot)
