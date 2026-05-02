from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from FSM.user import FSM

router = Router()

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Удалить анкету'),]
        ],
        resize_keyboard=True,
    )
    return keyboard

@router.message(F.text == 'Удалить анкету')
async def btn(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Анкета удалена!\nЕсли хотите начать заново, введите /start', reply_markup=ReplyKeyboardRemove())


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, Я бот для изучения английского\nВведите свое имя:')

    await state.set_state(FSM.name)

@router.message(FSM.name, F.text)
async def process1(message: Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer('Имя должно иметь только буквы!')
        return

    await state.update_data(name=name)

    await message.answer('Хорошо, Я хочу узнать твой уровень.\nВведите свой уровень:')
    await state.set_state(FSM.level)


@router.message(FSM.level, F.text)
async def process2(message: Message, state: FSMContext):
    level = message.text.upper()
    levels = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2' ]
    if level not in levels:
        await message.answer('Введите корректный уровень(A0, A1, A2, B1, B2, C1, C2)!')
        return

    await state.update_data(level=level)

    await message.answer('Круто, Какая у тебя цель?')
    await state.set_state(FSM.target)

@router.message(FSM.target, F.text)
async def process3(message: Message, state: FSMContext):
    await state.update_data(target=message.text)

    data = await state.get_data()
    name = data['name']
    level = data['level']
    target = data['target']

    await message.answer(f'Ваше имя: {name}\nВаш уровень: {level}\nВаша цель: {target}', reply_markup=get_reply_keyboard())
    await state.clear()