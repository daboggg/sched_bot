from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import date
from core.keyboards.inline import kb_get_calendar
from core.utils.statesform import StepsDateTime

basic_router = Router()


# Стартовое меню, выводит две кнопки: Интервал, Дата
@basic_router.message(Command(commands=['start']))
async def cmd_get_start(message: Message) -> None:
    await message.answer(f'Для получения сигнала через определенный интервал, выберите в меню <b>/interval</b>\n\n'
                         f'Для получения сигнала в определенную дату/время, выберите в меню <b>/date</b>',
                         parse_mode="HTML")


# выводит календарь для ввода даты
@basic_router.message(Command(commands=['date']))
async def cmd_date(message: Message, state: FSMContext) -> None:
    await message.answer("Введите дату сигнала", reply_markup=kb_get_calendar(date.today()))
    await state.set_state(StepsDateTime.GET_DATE)