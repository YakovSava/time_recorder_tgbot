from asyncio import run
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from plugins.binder import Binder
from plugins.states import StartState
from plugins.keyboards import KeyboardDataClass

binder = Binder(config_file='config.json')
bot = Bot(token=binder.sync_get_config()['token'])
dp = Dispatcher()

@dp.message(Command("start"), StateFilter(None))
async def start_reg(message: Message, state:FSMContext):
    await message.answer("Привет! Это бот для учёта времени. Для начала давайте зарегистрируемся!\n\nКак вас зовут (ФИО)?")
    await state.set_state(StartState.name)

@dp.message(StateFilter(StartState.name))
async def reg_success(message:Message, state:FSMContext):
    await message.answer(f'Отлично! Вы зарегестрированы как {message.text}!\nВот кнопки по которым предоставляется функционал!', keyboard=KeyboardDataClass.menu_keyboard)
    await state.clear()

@dp.callback_query(F.data == "in_job")
async def in_job(callback:CallbackQuery):
    await callback.message.answer('Мы записали что вы на работе!')

@dp.callback_query(F.data == "not_in_job")
async def not_in_job(callback:CallbackQuery):
    await callback.message.answer("Мы записали что вы не на работе!")

@dp.callback_query(F.data == "stat")
async def stat_handler(callback:CallbackQuery):
    await callback.message.answer("В процессе разработки!")

@dp.callback_query(F.data == "info")
async def info_handler(callback:CallbackQuery):
    await callback.message.answer("В процессе разработки!")

@dp.callback_query(F.data == "tp")
async def tp_handler(callback:CallbackQuery):
    await callback.message.answer("В процессе разработки!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())