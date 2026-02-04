from aiogram.fsm.state import StatesGroup, State

class RegistrationFSM(StatesGroup):
    waiting_name = State()
    waiting_email = State()
