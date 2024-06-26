from time import strftime, strptime, mktime, time
from asyncio import sleep
from aiogram import Bot
from plugins.binder import Binder
from plugins.database import Database

def gettime(t):
	return mktime(strptime(strftime("%d.%m.%y ")+t, "%d.%m.%y %H:%M"))

class ManagerError(Exception): pass

class Manager:

    def __init__(self, bot:Bot, timer_conf_filename:str=None, sqldb:Database=None):
        if timer_conf_filename is None:
            raise ManagerError("Timer config filename not found!")
        if sqldb is None:
            raise ManagerError("SQL Database not found!")
        self._bot = bot
        self._manager_binder = Binder(config_file=timer_conf_filename)
        self._sqldb = sqldb
        self._noted_ids = []

    async def worker(self) -> None:
        while True:
            config = await self._manager_binder.get_config()
            if (strftime("%H:%M") in config['morning']) or (time() > gettime(config['morning'][-1])):
                await self._mass_sender(config['morning_hello'])
            elif strftime("%H:%M") in config['evening']:
                await self._mass_sender(config['evening_hello'])
            elif strftime("%H:%M") in config['clear_noted']:
                self._noted_ids.clear()
            await sleep(config['timeout'])

    async def admin_send_test(self):
        config = await self._manager_binder.get_config()
        await self._mass_sender(config['tested_hello'], test=True)
        return self._noted_ids

    async def _mass_sender(self, text:str, test:bool=False) -> None:
        ids = await self._sqldb.get_all()
        for id in ids:
            if (id['id'] not in self._noted_ids) and (not id['injob']) and (not test):
                await self._sender(id['id'], text)
                self._noted_ids.append(id['id'])
            elif test:
                await self._sender(id['id'], f'Текст для {id["id"]}\nНа работе: {id["injob"]}\n{text}')

    async def _sender(self, id:int, text:str) -> None:
        await self._bot.send_message(chat_id=id, text=text)

    async def set_noted(self, id:int) -> None:
        self._noted_ids.append(id)
        
    def __del__(self):
        print('Manager destructor called!')