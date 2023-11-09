from aiogram import Bot
from aiogram.types import Message
from datetime import date
from core.keyboards.inline import kb_get_calendar

# Стартовое меню, выводит две кнопки: Интервал, Дата
async def cmd_get_start(message: Message) -> None:
    await message.answer(f'Для получения сигнала через определенный интервал, выберите в меню <b>/interval</b>\n\n'
                         f'Для получения сигнала в определенную дату/время, выберите в меню <b>/date</b>',
                         parse_mode="HTML")


# выводит календарь для ввода даты
async def cmd_date(message: Message) -> None:
    await message.answer("Введите дату сигнала", reply_markup=kb_get_calendar(date(2023,8,1)))
