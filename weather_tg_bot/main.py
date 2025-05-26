from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from weather_tg_bot.config import config
from weather_tg_bot.parser import WeatherParser

wp = WeatherParser()
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message()
async def get_weather(message: Message) -> None:
    await message.answer(await wp.get_weather(message.text))


async def main() -> None:
    """Запуск бота."""
    bot = Bot(token=config.tg_bot_token)
    await wp.init()
    await dp.start_polling(bot)
