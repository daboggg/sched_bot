import logging.config
from aiogram import Router, F
from aiogram.types import CallbackQuery
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.callback')

callback_router = Router()


# колбэк без исполнения
@callback_router.callback_query(F.data == 'empty')
async def cb_empty(callback: CallbackQuery) -> None:
    await callback.answer()
    logger.info('empty callback')


