from asyncio import run
from aiosqlite import connect, Row

class Database:

    def __init__(self, database_name:str="db.db"):
        run(self._async_init(database_name))

    async def _async_init(self, db_name:str) -> None:
        self._db = await connect(database=db_name, check_same_thread=False)
        self._db.row_factory = Row
        self._cursor = await self._db.cursor()
        await self._create_table()

    async def _create_table(self) -> None:
        await self._cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            injob INT
        )""")
        await self._db.commit()

    async def reg(self, id:int, name:str) -> None:
        await self._cursor.execute("""INSERT INTO users VALUES (?, ?, 0)""", (str(id), name))
        await self._db.commit()

    async def delete(self, id:int) -> None:
        await self._cursor.execute(f"DELETE FROM users WHERE id = '{str(id)}'")
        await self._db.commit()

    async def exists(self, id: int) -> bool:
        return (await self.get(id)) is not None

    async def get(self, id: int):
        await self._cursor.execute(f"SELECT * FROM users WHERE id = '{id}'")
        return await self._cursor.fetchone()

    async def get_all(self):
        await self._cursor.execute(f"SELECT * FROM users")
        return await self._cursor.fetchall()