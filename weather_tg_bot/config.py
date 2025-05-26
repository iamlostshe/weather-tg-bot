"""Глобальные настройки бота."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Глобальные настройки бота.

    Подгружаются один раз при запуске бота из .env файла.

    - tg_bot_token: Токен Telegram Bot API.
    - open_weather_token: Токен open weather API.
    """

    tg_bot_token: str
    open_weather_token: str


config: Config = Config(_env_file=".env")
