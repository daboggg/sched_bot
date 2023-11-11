import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.handlers.date import date_router
from core.middlewares.apschedmiddleware import SchedulerMiddleware

from core.handlers.basic import  basic_router

from core.settings import settings
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

    # scheduler = AsyncIOScheduler(
    #     jobstores={'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')},
    #     # executors={'default': AsyncIOExecutor()},
    #     executors={'default': ThreadPoolExecutor(max_workers=10,pool_kwargs=None)},
    #     timezone="Europe/Moscow")
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()

    dp = Dispatcher()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(
        basic_router,
        date_router,
    )

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(ex)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
