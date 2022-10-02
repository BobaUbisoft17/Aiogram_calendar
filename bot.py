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
    await Get_schedule.date.set()
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await message.answer(
        text="Выберите дату: ",
        reply_markup=CalendarMarkup(current_month, current_year).build.kb,
    )


@dp.message_handler()
async def another(message: types.Message):
    await message.answer(1)


@dp.callback_query_handler(state=Get_schedule.date)
async def get_date(callback: types.CallbackQuery, state: FSMContext):
    mes = callback.data
    if "date" in mes:
        await state.finish()
        await callback.message.answer(text=callback.data.split()[1])
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    elif "back" in mes or "next" in mes:
        await get_next_month(callback)


async def get_next_month(callback: types.CallbackQuery):
    month, year = map(int, callback.data.split()[1].split("."))
    if "next" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=CalendarMarkup.next_month(month, year).kb
        )
    elif "back" in callback.data:
        await callback.message.edit_reply_markup(
            reply_markup=CalendarMarkup.previous_month(month, year).kb
        )


"""@dp.callback_query_handler(text_contains="back")
async def previous_month(callback: types.CallbackQuery):
    month, year = map(int, callback.data.split()[1].split("."))
    await callback.message.edit_reply_markup(reply_markup=)"""


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
