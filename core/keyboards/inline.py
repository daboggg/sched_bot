import calendar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date

from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.app_data import days_of_week, months_of_year, months_of_year_full_name

# инлайн клавиатура календарь, выбор даты
from core.utils.callbackdata import ChangeMonthCallbackData, SelectMonthCallbackData, ChangeYearCallbackData


def kb_get_calendar(s_date: date) -> InlineKeyboardMarkup:
    day_of_week, month_range, = calendar.monthrange(s_date.year, s_date.month)
    today = date.today()
    week = []
    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='<', callback_data=ChangeMonthCallbackData(increase=False, year=s_date.year,
                                                                                 month=s_date.month).pack()),
            InlineKeyboardButton(text=f'{months_of_year[s_date.month - 1]} {s_date.year}',
                                 callback_data=SelectMonthCallbackData(year=s_date.year).pack()),
            InlineKeyboardButton(text='>', callback_data=ChangeMonthCallbackData(increase=True, year=s_date.year,
                                                                                 month=s_date.month).pack())
        ],
        [InlineKeyboardButton(text=day, callback_data='empty') for day in days_of_week]
    ])
    for d in range(1 - day_of_week, month_range + 1):
        if len(week) == 7:
            ikm.inline_keyboard.append(week)
            week = []
        if today.year == s_date.year and today.month == s_date.month:
            if d < today.day:
                week.append(InlineKeyboardButton(text=' ', callback_data='empty'))
            else:
                if today.day == d:
                    week.append(InlineKeyboardButton(text=f'[{d}]', callback_data='empty'))
                else:
                    week.append(InlineKeyboardButton(text=f'{d}', callback_data='empty'))
        else:
            if d <= 0:
                week.append(InlineKeyboardButton(text=' ', callback_data='empty'))
            else:
                week.append(InlineKeyboardButton(text=f'{d}', callback_data='empty'))

    for d in range(7 - len(week)):
        week.append(InlineKeyboardButton(text=' ', callback_data='empty'))
    ikm.inline_keyboard.append(week)
    ikm.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel')])

    return ikm


def kb_select_month(year: int) -> InlineKeyboardMarkup:
    today = date.today()
    row = []
    start_month = today.month if today.year == year else 1
    ikm = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='<', callback_data=ChangeYearCallbackData(increase=False, year=year).pack()),
            InlineKeyboardButton(text=f'{year}', callback_data='select_year'),
            InlineKeyboardButton(text='>', callback_data=ChangeYearCallbackData(increase=True, year=year).pack())
        ],
    ])
    for month in months_of_year_full_name[start_month - 1:]:
        if len(row) == 4:
            ikm.inline_keyboard.append(row)
            row = []
        if today.year == year and month == months_of_year_full_name[today.month - 1]:
            row.append(InlineKeyboardButton(text=f'[{month}]', callback_data='empty'))
        else:
            row.append(InlineKeyboardButton(text=month, callback_data='empty'))
    ikm.inline_keyboard.append(row)
    ikm.inline_keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel')])
    return ikm


def kb_select_year() -> InlineKeyboardMarkup:
    year = date.today().year
    ikb = InlineKeyboardBuilder()
    for i in range(0, 10):
        ikb.button(text=f'{year + i}', callback_data='empty')
    ikb.button(text='Отмена', callback_data='cancel')
    ikb.adjust(5, 5, 1)
    return ikb.as_markup()
