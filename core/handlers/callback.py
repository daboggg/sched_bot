from aiogram.types import CallbackQuery

# колбэк без исполнения
async def cb_empty(callback: CallbackQuery):
    await callback.answer()


# колбэк для смены месяца (+1 или -1 месяц)
async def cb_change_month(callback: CallbackQuery):
    pass

