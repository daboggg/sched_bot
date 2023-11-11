import logging.config
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.keyboards.inline import kb_confirm_date_time
from core.utils.statesform import StepsDateTime
from log_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('core.handlers.datetime_message')

datetime_message_router = Router()


async def send_message_date(bot: Bot, chat_id: int, text: str) -> None:
    await bot.send_message(chat_id, text)


#  ввод текста
@datetime_message_router.message(StepsDateTime.GET_TEXT)
async def cb_get_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    context = await state.get_data()
    await message.answer(f"выбранная дата: {context.get('year')}-"
                                     f"{context.get('month')}-{context.get('day')}\n"
                                     f"выбранное время: {context.get('hour')}:{context.get('minute')}:00\n"
                                     f"набранный текст: {message.text}\n"
                                     f"подтвердите ввод",
                         reply_markup=kb_confirm_date_time())
    await state.set_state(StepsDateTime.CONFIRM_DATETIME)
    logger.info(f'набран текст: {message.text}')