import asyncio
import logging.config

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.middlewares.apschedmiddleware import SchedulerMiddleware

from core.handlers.basic import cmd_get_start, cmd_date
from core.handlers.callback import *

from core.settings import settings
from core.utils.callbackdata import *
from core.utils.commands import set_commands
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')


async def start_bot(bot: Bot) -> None:
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


async def start() -> None:
    bot = Bot(settings.bots.bot_token, parse_mode='HTML')

    # scheduler = AsyncIOScheduler(jobstores={'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.start()

    dp = Dispatcher()
    # dp.update.middleware.register(SchedulerMiddleware(scheduler))


    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    
    dp.message.register(cmd_get_start, Command(commands=['start']))
    dp.message.register(cmd_date, Command(commands=['date']))
    dp.callback_query.register(cb_empty, F.data == 'empty')
    dp.callback_query.register(cb_change_month, ChangeMonthCallbackData.filter())
    dp.callback_query.register(cb_select_month, SelectMonthCallbackData.filter())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()



if __name__ == '__main__':
    asyncio.run(start())
