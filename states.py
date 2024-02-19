from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    img_prompt = State()
    room_type = State()
    room_style = State()
    get_img = State()