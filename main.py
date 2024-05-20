from asyncio import run
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from plugins.binder import Binder

binder = Binder(config_file='config.json')
bot = Bot(token=binder.sync_get_config()['token'])
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())