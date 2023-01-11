from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from decouple import config

TOKEN = config('API_TOKEN')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

path_accounts = r'D:\Python\english\english_bot\accounts.txt'
path_levels = r'D:\Python\project\Learn_English_bot\levels.txt'
id_user = []
lvl_user = []

inline_back = types.InlineKeyboardMarkup()
inline_back.add(types.InlineKeyboardButton('Back👈', callback_data='back'))

choice_md = types.InlineKeyboardMarkup(row_width=1)
md_1 = types.InlineKeyboardButton('Выбрать новый уровень английского🤔', callback_data='new')
md_2 = types.InlineKeyboardButton('Продолжить обучение прошлого уровня😌', callback_data='old')
choice_md.add(md_1, md_2)

inline_keyboard = types.InlineKeyboardMarkup()
inline_btn_1 = types.InlineKeyboardButton('Войти в аккаунт📲', callback_data='enter')
inline_btn_2 = types.InlineKeyboardButton('Зарегистрироваться📄', callback_data='registration')
inline_keyboard.add(inline_btn_1, inline_btn_2)

inline_levels = types.InlineKeyboardMarkup(row_width=1)
level_1 = types.InlineKeyboardButton('A1(Beginner)', callback_data='A1')
level_2 = types.InlineKeyboardButton('A2(Elementary)', callback_data='A2')
level_3 = types.InlineKeyboardButton('B1(Intermediate)', callback_data='B1')
level_4 = types.InlineKeyboardButton('B2(Upper-Intermediate)', callback_data='B2')
level_5 = types.InlineKeyboardButton('C1(Advanced)', callback_data='C1')
level_6 = types.InlineKeyboardButton('C2(Proficiency)', callback_data='C2')
inline_levels.add(level_1, level_2, level_3, level_4, level_5, level_6)

class Register(StatesGroup):
    enter = State()
    register_account = State()

class Level_english(StatesGroup):
    choice_lvl = State()
    choice = State()
    mode = State()

def check_lvl(data):
    with open(path_levels, 'r') as file:
        if f'{data}, {id_user[0]}' in str(file.readlines()):
            return False
        else:
            return True
def lvl():
    lvl_keyboard = types.InlineKeyboardMarkup()
    with open(path_levels, 'r+') as file:
        for i in str(file.readlines()).split(','):
            lvl_user.append(i)
            if str(id_user[0]) in i:
                lvl_keyboard.add(types.InlineKeyboardButton(str(lvl_user[0])[2:], callback_data=str(lvl_user[0])[2:]))
                lvl_user.clear()
    return lvl_keyboard

@dp.message_handler(commands=['start'], state='*')
async def send_welcome(msg: types.Message, state=FSMContext):
    await msg.reply('Привет! Я бот для изучения английской лексики по разным уровням.', reply_markup=inline_keyboard)

#Регистрация или вход в аккаунт
@dp.callback_query_handler(lambda c: c.data == 'back')
async def back_registration(msg: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await msg.message.edit_text('Выберите еще раз что вас интересует!', reply_markup=inline_keyboard)
    
@dp.callback_query_handler(lambda c: c.data == 'registration', state='*')
async def register(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text("Введите свой ник для нового аккаунта!")
    await Register.register_account.set()

@dp.callback_query_handler(lambda c: c.data == 'enter', state='*')
async def enter_account(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text("Введите свой ник для аккаунта!")
    await Register.enter.set()

@dp.message_handler(state=Register.register_account)
async def create_account(msg: types.Message, state=FSMContext):
    with open(path_accounts, 'r+') as file:
        if str(msg.from_id) in str(file.readlines()):
            await msg.answer("Извините на этом устройстве уже есть аккаунт🤨. Попробуйте ввойти в него!", reply_markup=inline_back)
            await state.finish()
        else:
            id_user.clear() 
            file.write(f'{msg.from_id}, {msg.text}\n')
            await msg.answer(f'Вы зарегистрировались! Ваш ник {msg.text}')
            id_user.append(msg.from_id)
            await msg.answer("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
            await Level_english.choice_lvl.set()

@dp.message_handler(state=Register.enter)
async def account(msg: types.Message, state=FSMContext):
    with open(path_accounts, 'r+') as file:
        if f'{msg.from_id}, {msg.text}' in str(file.readlines()):
            id_user.clear()
            await msg.answer(f'Вы успешно вошли в ваш аккаунт, {msg.text}!', reply_markup=choice_md)
            id_user.append(msg.from_id)
            await Level_english.choice.set()
        else:
            await msg.answer(f'Такого ника нет в нашей базе данных🤨. Попробуйте ввести снова ник!')
            await Register.enter.set()
            
# Выбор уровня английского при первой регистрации или проверка уровня при входе
@dp.callback_query_handler(state=Level_english.choice_lvl)
async def level_choice(msg: types.CallbackQuery, state=FSMContext):
    if check_lvl(msg.data) == True:
        with open(path_levels, 'r+') as file:
            file.read()
            file.write(f'{msg.data}, {id_user[0]}\n')
        await msg.message.edit_text('Я тебя понял')
        await state.finish()
    else:
        await msg.message.edit_text('Извините, вы уже выбирали этот уровень английского! Выберите что вас интересует!😉', reply_markup=choice_md)
        await Level_english.choice.set()

@dp.callback_query_handler(state=Level_english.choice)
async def level_choice(msg: types.CallbackQuery, state=FSMContext):
    if msg.data == 'new':
        await msg.message.edit_text("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
        await Level_english.choice_lvl.set()
    else:
        await msg.message.edit_text("Выберите уровень английского, который продолжишь изучать!🇬🇧", reply_markup=lvl())
        await Level_english.mode.set()

@dp.callback_query_handler(state=Level_english.mode)
async def mode_task(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.answer('Отлично, работает!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
