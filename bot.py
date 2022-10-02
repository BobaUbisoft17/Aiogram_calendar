from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
import logging
import os

from tg_calendar import CalendarMarkup


logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("BOTTOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())


class Get_schedule(StatesGroup):
    date = State()
    group = State()


@dp.message_handler(commands=["start"])
async def hi_hendler(message: types.Message):
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await message.answer(
        text="Выберите дату: ",
        reply_markup=CalendarMarkup(current_month, current_year).build.kb,
    )


@dp.callback_query_handler()
async def get_date(callback: types.CallbackQuery, state: FSMContext):
    mes = callback.data
    if "date" in mes:
        await callback.message.answer(text=callback.data.split()[1])
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    elif "back" in mes or "next" in mes:
        await get_next_month(callback)


async def get_next_month(callback: types.CallbackQuery):
    month, year = map(int, callback.data.split()[1].split("."))
    calendar = CalendarMarkup(month, year)
    if "next" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=calendar.next_month().kb
        )
    elif "back" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=calendar.previous_month().kb
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
