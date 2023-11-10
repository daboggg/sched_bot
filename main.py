import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers.time_callback import time_callback_router
from core.middlewares.apschedmiddleware import SchedulerMiddleware

from core.handlers.basic import  basic_router
from core.handlers.callback import callback_router
from core.handlers.date_callback import date_callback_router

from core.settings import settings
from core.utils.commands import set_commands
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')


async def start_bot(bot: Bot) -> None:
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')
    logger.info('Бот запущен!')


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')
    logger.info('Бот остановлен!')


async def start() -> None:
    bot = Bot(settings.bots.bot_token, parse_mode='HTML')

    # scheduler = AsyncIOScheduler(jobstores={'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})
    # scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # scheduler.start()

    dp = Dispatcher()
    # dp.update.middleware.register(SchedulerMiddleware(scheduler))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        basic_router,
        callback_router,
        date_callback_router,
        time_callback_router,
    )

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(ex)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
