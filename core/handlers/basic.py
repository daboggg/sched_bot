from aiogram import Bot
from aiogram.types import Message


async def get_start(message: Message) -> None:
    # await bot.send_message(message.from_user.id, f'<tg-spoiler>Привет {message.from_user.first_name}. Рад тебя видеть!</tg-spoiler>')
    await message.answer(f'<b>Привет {message.from_user.first_name}. Рад тебя видеть!</b>')
    # await message.reply(f'<s>Привет {message.from_user.first_name}. Рад тебя видеть!</s>')
    # await message.answer(f'Для получения сигнала через определенный интервал, нажмите на кнопку \"Интервал\"\n'
    #                      f'Для получения сигнала в определенную дату/время, нажмите на кнопку \"Дата\"',
    #                      reply_markup=get_start_keyboard())



