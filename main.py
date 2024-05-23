from asyncio import run
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from plugins.binder import Binder
from plugins.states import StartState
from plugins.keyboards import KeyboardDataClass
from plugins.logger import Logger
from plugins.database import Database
from plugins.keyvaluedb import KVDatabase

logger = Logger(printed=True)
logger.log("Библиотеки импортированы")
logger.log("Лог инициализирован")

binder = Binder(config_file='config.json')
logger.log("Инициализирован класс Binder")
config = binder.sync_get_config()
kvdb = KVDatabase(filename=config['kvdb'])
sqldb = Database(database_name=config['database'])
bot = Bot(token=config['token'])
dp = Dispatcher()
logger.log("Инициализирован бот и диспетчер")

@dp.message(Command("start"), StateFilter(None))
async def start_reg(message: Message, state:FSMContext):
    await message.answer("Привет! Это бот для учёта времени. Для начала давайте зарегистрируемся!\n\nКак вас зовут (ФИО)?")
    await state.set_state(StartState.name)

@dp.message(StateFilter(StartState.name))
async def reg_success(message:Message, state:FSMContext):
    await message.answer(f'Отлично! Вы зарегестрированы как {message.text}!\nВот кнопки по которым предоставляется функционал!', reply_markup=KeyboardDataClass.menu_keyboard)
    await state.clear()

@dp.message(F.text == "Я на работе!")
async def in_job(message:Message):
    await message.answer('Мы записали что вы на работе!')

@dp.message(F.text == "Я не на работе!")
async def not_in_job(message:Message):
    await message.answer("Мы записали что вы не на работе!")

@dp.message(F.text == "Моя статистика")
async def stat_handler(message:Message):
    await message.answer("В процессе разработки!")

@dp.message(F.text == "Информация о боте")
async def info_handler(message:Message):
    await message.answer("В процессе разработки!")

@dp.message(F.text == "Техподдержка")
async def tp_handler(message:Message):
    await message.answer("В процессе разработки!")

async def main():
    logger.log("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.log("Бот запускается...")
    run(main())