from aiogram.fsm.state import State, StatesGroup

class User_fsm(StatesGroup):
    updating_form = State()
    updating_group = State()
    update_over = State()