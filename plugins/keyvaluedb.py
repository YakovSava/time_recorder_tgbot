from os.path import exists
from typing import Any
from aiofiles import open as aiopen

class KVDatabase:

    def __init__(self, filename:str="db.enc"):
        self._filename = filename
        if not exists(self._filename):
            with open(self._filename, 'w', encoding='utf-8') as file:
                file.write(self._encode('{}'))

    def _encode(self, data: str) -> str:
        return " ".join(map(lambda x: str(ord(x) << 5), list(data)))

    def _decode(self, encode_data: str) -> str:
        return "".join(map(lambda x: chr(int(x) >> 5), encode_data.split()))

    async def exists(self, id:int):
        try:
            return await self.get(str(id))
        except:
            return {'connects': [], 'discovers': []}

    async def set(self, key:str, value:Any) -> None:
        data = await self.get_all()
        data[key] = value
        async with aiopen(self._filename, 'w', encoding='utf-8') as file:
            await file.write(self._encode(str(data)))

    async def get(self, key:str) -> Any:
        async with aiopen(self._filename, 'r', encoding='utf-8') as file:
            return eval(self._decode(await file.read()))[key]

    async def get_all(self) -> dict:
        async with aiopen(self._filename, 'r', encoding='utf-8') as file:
            return eval(self._decode(await file.read()))

    async def delete(self, key:str) -> None:
        data = await self.get_all()
        del data[key]
        async with aiopen(self._filename, 'w', encoding='utf-8') as file:
            await file.write(self._encode(str(data)))