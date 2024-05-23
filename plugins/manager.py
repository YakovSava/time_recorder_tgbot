from time import time, strftime, gmtime
from aiogram import Bot
from plugins.binder import Binder

class ManagerError(Exception): pass

class Manager:

    def __init__(self, bot:Bot, timer_conf_filename:str=None):
        if timer_conf_filename:
            raise ManagerError("Timer config filename not found!")
        self._bot = bot

    async def worker(self):
        pass

    async def _mass_sender(self):
        pass

    async def _sender(self, id:int, text:str):
        await self._bot.send_message(chat_id=id, text="")