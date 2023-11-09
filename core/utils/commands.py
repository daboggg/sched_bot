from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Нажмите для начала работы'
        ),
        BotCommand(
            command='interval',
            description='сигнал через определенный интервал'
        ),
        BotCommand(
            command='date',
            description='сигнал в определенную дату/время'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())