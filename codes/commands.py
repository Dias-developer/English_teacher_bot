from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext


from service.check import client
from states.user import FSM

router = Router()

def is_english(text: str) -> bool:
    eng = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?\'')

    for symbol in text:
        if symbol not in eng:
            return False

    return True

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Remove')],
            [KeyboardButton(text='Practice')]
        ],
        resize_keyboard=True,
    )
    return keyboard

@router.message(F.text == 'Remove')
async def btn_remove(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Анкета удалена!\nЕсли хотите начать заново, введите /start', reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'Practice')
async def btn_practice(message: Message, state: FSMContext):
    await start_practice(message, state)


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, Я бот для изучения английского\nВведите свое имя:')

    await state.set_state(FSM.name)

@router.message(FSM.name, F.text)
async def process_name(message: Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer('Имя должно иметь только буквы!')
        return

    await state.update_data(name=name)

    await message.answer('Хорошо, Я хочу узнать твой уровень.\nВведите свой уровень:')
    await state.set_state(FSM.level)


@router.message(FSM.level, F.text)
async def process_level(message: Message, state: FSMContext):
    level = message.text.upper()
    levels = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2' ]
    if level not in levels:
        await message.answer('Введите корректный уровень(A0, A1, A2, B1, B2, C1, C2)!')
        return

    await state.update_data(level=level)

    await message.answer('Круто, Какая у тебя цель?')
    await state.set_state(FSM.target)

@router.message(FSM.target, F.text)
async def process_target(message: Message, state: FSMContext):
    await state.update_data(target=message.text)

    data = await state.get_data()
    name = data['name']
    level = data['level']
    target = data['target']

    await message.answer(f'Ваше имя: {name}\nВаш уровень: {level}\nВаша цель: {target}\n\n'
                         'Если хотите попрактиковаться то введите /practice или нажмите кнопку в меню!', reply_markup=get_reply_keyboard())

@router.message(Command('practice'))
async def start_practice(message: Message, state:FSMContext):
    await message.answer('Напиши мне предложение на английском!')
    await state.set_state(FSM.practice)

@router.message(FSM.practice, F.text)
async def start_practice_save(message: Message, state:FSMContext):
    user_text = message.text

    if not is_english(user_text):
        await message.answer('Пиши на английском!')
        return

    if len(user_text.split()) < 3:
        await message.answer('Напиши более длинное предложение!')
        return

    res = await client.chat.completions.create(
        model='llama-3.1-8b-instant',
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an English teacher. "
                    "Your student is between (A0, A1, A2, B1, B2) level. "
                    "1. Correct grammar mistakes. "
                    "2. Explain mistakes simply. "
                    "3. Rewrite correct sentence. "
                    "4. Ask a follow-up question."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    ai_reply = res.choices[0].message.content

    await message.answer(ai_reply)

    await state.clear()