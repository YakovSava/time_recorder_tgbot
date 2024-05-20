from json import loads
from aiofiles import open as aiopen

class BinderCriticalError(BaseException): pass
class BinderError(Exception): pass

class Binder:

	def __init__(self, config_file:str=None):
		if config_file is None:
			raise BinderCriticalError('Config file is None!')
		self._name = config_file

	async def _read(self, filename:str) -> str:
		async with aiopen(filename, 'r', encoding='utf-8') as file:
			return await file.read()

	async def _write(self, filename:str, data:str) -> None:
		async with aiopen(filename, 'w', encoding='utf-8') as file:
			await file.write(data)

	async def get_config(self) -> dict:
		return loads(await self._read(self._name))

	def sync_get_config(self) -> dict:
		with open(self._name, 'r', encoding='utf-8') as file:
			return loads(file.read())