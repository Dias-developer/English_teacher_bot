from aiogram.fsm.state import StatesGroup, State

class FSM(StatesGroup):
    name = State()
    level = State()
    target = State()
    practice = State()
