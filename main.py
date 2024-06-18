from time import strftime
from asyncio import run, gather, create_task
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from plugins.binder import Binder
from plugins.states import StartState, TPState
from plugins.keyboards import KeyboardDataClass
from plugins.logger import Logger
from plugins.database import Database
from plugins.keyvaluedb import KVDatabase
from plugins.manager import Manager

from analyze_plugins.analyze import calculate_times

logger = Logger(printed=True)
logger.log("Библиотеки импортированы")
logger.log("Лог инициализирован")

binder = Binder(config_file='config.json')
logger.log("Инициализирован класс Binder")
config = binder.sync_get_config()
logger.log('Получен лог')
kvdb = KVDatabase(filename=config['kvdb'])
logger.log('KVDB инициализирован')
sqldb = Database(database_name=config['database'])
logger.log('SQL база данных инициализирована')
bot = Bot(token=config['token'])
dp = Dispatcher()
logger.log("Инициализирован бот и диспетчер")
mngr = Manager(bot, timer_conf_filename=config['time_config'], sqldb=sqldb)
logger.log("Инициализирован менеджер")

@dp.message(Command("start"), StateFilter(None))
async def start_reg(message: Message, state:FSMContext):
    if await sqldb.exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы в этом боте!", reply_markup=KeyboardDataClass.menu_keyboard)
    else:
        await message.answer("Привет! Это бот для учёта времени. Для начала давайте зарегистрируемся!\n\nКак вас зовут (ФИО)?", reply_markup=KeyboardDataClass.DELETE)
        await state.set_state(StartState.name)

@dp.message(StateFilter(StartState.name))
async def reg_success(message:Message, state:FSMContext):
    await message.answer(f'Отлично! Вы зарегистрированы как "{message.text}"!\nВот кнопки по которым предоставляется функционал!', reply_markup=KeyboardDataClass.menu_keyboard)
    await sqldb.reg(int(message.from_user.id), message.text)
    await state.clear()

@dp.message(F.text == "Узнать статус")
async def check_status(message:Message):
    if (await sqldb.exists(message.from_user.id)):
        if (await sqldb.get(message.from_user.id))['injob']:
            await message.answer('Вы на работе!')
        else:
            await message.answer('Вы не на работе!')
    else:
        await message.answer('Вы не зарегестрированы!\nНажмите сюда:\n\n/start', reply_markup=KeyboardDataClass.DELETE)

@dp.message(F.text == "Я на работе!")
async def in_job(message:Message):
    if await sqldb.exists(message.from_user.id):
        if (await sqldb.get(message.from_user.id))['injob']:
            await message.answer('Вы уже на работе!')
        else:
            id_acc:dict = await kvdb.exists(message.from_user.id)
            id_acc['connects'].append(strftime("%H:%M %d.%m.%y"))
            await kvdb.set(str(message.from_user.id), id_acc)
            await sqldb.injob(message.from_user.id)
            await message.answer('Мы записали что вы на работе!')
    else:
        await message.answer("Вы не зарегистрированы и не можете пользоваться ботом!\nНажмите сюда:\n\n/start", reply_markup=KeyboardDataClass.DELETE)

@dp.message(F.text == "Я не на работе!")
async def not_in_job(message:Message):
    if await sqldb.exists(message.from_user.id):
        if (await sqldb.get(message.from_user.id))['injob']:
            id_acc: dict = await kvdb.exists(message.from_user.id)
            id_acc['discovers'].append(strftime("%H:%M %d.%m.%y"))
            await kvdb.set(str(message.from_user.id), id_acc)
            await sqldb.notinjob(message.from_user.id)
            await message.answer("Мы записали что вы не на работе!")
        else:
            await message.answer('Вы и так не на работе!')
    else:
        await message.answer("Вы не зарегистрированы и не можете пользоваться ботом!\nНажмите сюда:\n\n/start", reply_markup=KeyboardDataClass.DELETE)

@dp.message(F.text == "Моя статистика")
async def stat_handler(message:Message):
    if await sqldb.exists(message.from_user.id):
        stat = (await calculate_times(await kvdb.get_all()))[str(message.from_user.id)]
        msg = "Вы проработали:\n"
        for date, hours in list(stat.items())[-2:]:
            msg += f"{date} - {hours} часа\n"
        await message.answer(msg)
    else:
        await message.answer('Я не знаю кто вы, потому не могу дать статистику!\nДавайте зарегистрируемся! Нажмите на:\n\n/start')

@dp.message(F.text == "Информация о боте")
async def info_handler(message:Message):
    if await sqldb.exists(message.from_user.id):
        await message.answer("""Общая информация о боте:
__Юридическая информация:__
Программист: [Савельев Яков (YakovSava)](https://github.com/YakovSava/)
Создано специально для *CityBox*

*Copyright*
*MIT License*

__Техническая информация:__
Язык программирования: *Python*
Используемые фреймворки: *Aiogram, Asyncio, SQLite3*
""", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Давайте прежде чем получать информацию о боте, зарегистрируемся?\nНапример нажмите сюда:\n\n/start")

@dp.message(F.text == "Техподдержка", StateFilter(None))
async def tp_handler(message:Message, state:FSMContext):
    await message.answer("Напишите ваш вопрос в техподдержку и вам ответят как можно скорее")
    await state.set_state(TPState.quest)

@dp.message(StateFilter(TPState.quest))
async def tp_state_handler(message:Message, state:FSMContext):
    await message.answer('Ваш вопрос отправлен в техподдержку!')
    await state.clear()
    for admin_id in config['admins']:
        await bot.send_message(chat_id=admin_id, text=f'Вопрос от пользователя <{message.from_user.id}>\n\n{message.text}\n\nОтветить можно командой "answer <id> <ответ>"')

@dp.message(F.text.startswith('admin'))
async def admin_handler(message:Message):
    cmds = message.text.lower().split()
    if cmds[1] == 'getall':
        await message.answer(f"""* Ответ команды для администрации *
{await kvdb.get_all()}""", parse_mode=ParseMode.MARKDOWN)
    elif cmds[1] == 'analyze':
        await message.answer(f"""* Ответ команды для администрации *
{await calculate_times(await kvdb.get_all())}""", parse_mode=ParseMode.MARKDOWN)
    elif cmds[1] == 'time':
        await message.answer(f"""* Ответ команды для администрации *
Текущее время: {strftime("%H:%M %d.%m.%y")}""", parse_mode=ParseMode.MARKDOWN)
    elif cmds[1] == 'manager':
        await message.answer(f"""* Ответ команды для администрации *
Записанные ID: {await mngr.admin_send_test()}
** Рассылка выслана! **""", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("* Ошибка *\nКоманда не существует", parse_mode=ParseMode.MARKDOWN)

@dp.message(F.text.startswith('answer'))
async def admin_answer(message:Message):
    cn = message.text.split(maxsplit=2)
    try:
        await bot.send_message(chat_id=int(cn[1]), text=f'Ответ от администратора:\n{cn[2]}')
    except:
        await message.answer('Ответ не отправлен')
    else:
        await message.answer('Ответ отправлен!')

async def main():
    logger.log("Бот запущен!")
    await gather(
        create_task(dp.start_polling(bot)),
        create_task(mngr.worker())
    )

if __name__ == "__main__":
    logger.log("Бот запускается...")
    run(main())