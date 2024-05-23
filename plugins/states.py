from aiogram.fsm.state import State, StatesGroup

class StartState(StatesGroup):
    name = State()
