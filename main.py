import os
from random import*
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from decouple import config
from googletrans import Translator

TOKEN = config('API_TOKEN')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

path_accounts = r'data\accounts.txt'
path_levels = r'data\levels.txt'
path_description = r'description.txt'
path_info = r'levels_english'
path_count_words = r'data\count_words.txt'
id_user = []
lvl_user = []
words_all = []
word_origin = []
word_text = []
count = []
buttons = []
correct_word = []
answer_on_correct = ['Молодец😊', 'Так держать😙', 'Я тобой горжусь😊', 'Неплохо😏', 'Отлично😊']
answer_on_wrong = ['Ты немного ошибся😶', 'Нет😥', 'Ну нет же🙄', 'Неа😥', 'Ты ошибся🤔']

inline_back = types.InlineKeyboardMarkup()
inline_back.add(types.InlineKeyboardButton('Back👈', callback_data='back'))

choice_md = types.InlineKeyboardMarkup(row_width=1)
md_1 = types.InlineKeyboardButton('Выбрать новый уровень английского🤔', callback_data='new')
md_2 = types.InlineKeyboardButton('Продолжить обучение прошлого уровня😌', callback_data='old')
choice_md.add(md_1, md_2)

inline_mode = types.InlineKeyboardMarkup(row_width=1)
mod_1 = types.InlineKeyboardButton('Карточки🃏', callback_data='cards')
mod_2 = types.InlineKeyboardButton('Заучивание👨‍🏫', callback_data='memorization')
mod_3 = types.InlineKeyboardButton('Тест📌', callback_data='test')
mod_4 = types.InlineKeyboardButton('Описания каждого режима📰', callback_data='description')
inline_mode.add(mod_1, mod_2, mod_3, mod_4)

inline_cards = types.InlineKeyboardMarkup(row_width=1)
cards_1 = types.InlineKeyboardButton('Режим заучивание👨‍🏫', callback_data='memorization')
cards_2 = types.InlineKeyboardButton('Back👈', callback_data='back')
inline_cards.add(cards_1, cards_2)

inline_test = types.InlineKeyboardMarkup()
test_1 = types.InlineKeyboardButton('Тест📌', callback_data='test')
test_2 = types.InlineKeyboardButton('Back👈', callback_data='back')
inline_test.add(test_1, test_2)

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
    mode_1 = State()
    mode_2 = State()
    mode_memory = State()
    check_otvet = State()
    repeat = State()
    test = State()

def check_lvl(data):
    with open(path_levels, 'r') as file:
        if f'{data},{id_user[0]}' in str(file.readlines()):
            return False
        else:
            return True
def lvl():
    lvl_keyboard = types.InlineKeyboardMarkup()
    with open(path_levels, 'r') as file:
        for i in file.readlines():
            if str(id_user[0]) in i:
                for el in i.strip('\n').split(','):
                    if len(el) == 2:
                        lvl_keyboard.add(types.InlineKeyboardButton(el, callback_data=el))
    lvl_keyboard.add(types.InlineKeyboardButton('Back👈', callback_data='back'))
    return lvl_keyboard

def translate_word(words):
    words_all.clear()
    word_text.clear()
    word_origin.clear()
    translator = Translator()
    translations = translator.translate(text=words, src='en', dest='ru')
    for translation in translations:
        word_origin.append(translation.origin.lower())
        word_text.append(translation.text.lower())
        words_all.append(f'{translation.origin.capitalize()} - {translation.text.lower()}')
    return words_all

def word_trans(index):
    info = os.listdir(path_info)
    for i in info:
        if f'{lvl_user[0]}.txt' in i:
            with open(rf'{path_info}\{i}', 'r') as file_2:
                dat = file_2.readline().split(',')
                content = ''
                if type(index) == int:
                    for el in translate_word(dat[:index]):
                        content += f'{el}\n'
                else:
                    for el in translate_word(dat[int(index[0]):int(index[1])]):
                        content += f'{el}\n'
                return content

def count_words():
    count.clear()
    with open(path_count_words, 'r') as file_1:
        lines = file_1.readlines()
    with open(path_count_words, 'w') as file_2:
        for line in lines:
            line = line.strip('\n')
            if f'{id_user[0]},{lvl_user[0]}' in line:
                a =  line.strip('\n').split(',')
                tt = []
                for el in a:
                    g = el.split(':')
                    if len(g) == 2:
                        for i in g:
                            tt.append(str(int(i)+15))
                        tt_1 = ':'.join(tt)
                        count.append(tt_1)
                    else:
                        count.append(el)
                count_1 = ','.join(count)
                if int(tt[1]) >= 105:
                    with open(path_levels, 'r') as file_3:
                        h = file_3.readlines()
                    with open(path_levels, 'w') as file_4:
                        for h_1 in h:
                            h_1 = h_1.strip('\n')
                            if lvl_user[0] in h_1:
                                pass
                            else:
                                file_4.write(f'{h_1}\n')
                else:
                    file_2.write(f'{count_1}\n')
            else:
                file_2.write(f'{line}\n')
    return tt

def create_question_memory(word):
        keyboard = types.ReplyKeyboardMarkup()
        word_origin_1 = word_origin[:]
        f = []
        for slovo in words_all:
            if word in slovo:
                g = slovo.replace(' ', '').split('-')
                word_origin_1.remove(g[0].lower())
                f.append(g[0].lower())
                buttons.append(types.KeyboardButton(g[0].lower()))
                break
        for i in range(3):
            random_choice = choice(word_origin_1).lower()
            h  = types.KeyboardButton(random_choice)
            buttons.append(h)
            word_origin_1.remove(random_choice)
            f.append(random_choice)
        for el in f:
            word_origin_1.append(el)
        for el in range(4):
            a = choice(buttons)
            keyboard.add(a)
            buttons.remove(a)
        return keyboard
                     
@dp.message_handler(commands=['start'], state='*')
async def send_welcome(msg: types.Message, state=FSMContext):
    await msg.answer('Привет! Я бот для изучения английской лексики по разным уровням.', reply_markup=inline_keyboard)

#Выходы из разных ситуаций с помощью кнопки "Back"
@dp.callback_query_handler(lambda c: c.data == 'back', state=[Level_english.mode_1, Level_english.mode_memory, Level_english.test])
async def back_registration(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)

@dp.callback_query_handler(lambda c: c.data == 'back', state=Level_english.mode_2)
async def back_registration(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text('Выберите еще раз что вас интересует!', reply_markup=choice_md)
    await Level_english.choice.set()
    
@dp.callback_query_handler(lambda c: c.data == 'back', state=Level_english.repeat)
async def back_registration(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)
    await Level_english.mode_1.set()

@dp.callback_query_handler(lambda c: c.data == 'back')
@dp.callback_query_handler(state=Register.enter)
async def back_registration(msg: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await msg.message.edit_text('Выберите еще раз что вас интересует!', reply_markup=inline_keyboard)

#Регистрация или вход в аккаунт    
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
            file.write(f'{msg.from_id},{msg.text.lower()}\n')
            await msg.answer(f'Вы зарегистрировались! Ваш ник {msg.text}')
            id_user.append(msg.from_id)
            await msg.answer("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
            await Level_english.choice_lvl.set()

@dp.message_handler(state=Register.enter)
async def account(msg: types.Message, state=FSMContext):
    with open(path_accounts, 'r+') as file:
        cons = file.readlines()
        for con in cons:
            if f'{msg.from_id},{msg.text.lower()}' == con.strip('\n'):
                id_user.clear()
                await msg.answer(f'Вы успешно вошли в ваш аккаунт, {msg.text}!', reply_markup=choice_md)
                id_user.append(msg.from_id)
                await Level_english.choice.set()
            else:
                await msg.answer(f'Такого ника нет в нашей базе данных🤨. Вернитесь на главное меню!', reply_markup=inline_back)
                await Register.enter.set()
            
# Выбор уровня английского при первой регистрации или проверка уровня при входе
@dp.callback_query_handler(state=Level_english.choice_lvl)
async def level_choice(msg: types.CallbackQuery, state=FSMContext):
    lvl_user.clear()
    if check_lvl(msg.data) == True:
        with open(path_levels, 'r+') as file:
            file.read()
            file.write(f'{msg.data},{id_user[0]}\n')
        lvl_user.append(msg.data)
        await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)
        await Level_english.mode_1.set()
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
        await Level_english.mode_2.set()

@dp.callback_query_handler(state=Level_english.mode_2)
async def enter_mode(msg: types.CallbackQuery, state=FSMContext):
    lvl_user.clear()
    lvl_user.append(msg.data)
    await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)
    await Level_english.mode_1.set()

#Выбор режима изучения
@dp.callback_query_handler(lambda c: c.data == 'description', state=[Level_english.mode_1, Level_english.mode_memory, Level_english.test])
async def mode_description(msg: types.CallbackQuery, state=FSMContext):
    with open(path_description, 'r', encoding='utf-8') as file:
        a = file.read()
    await msg.message.edit_text(a, parse_mode='HTML', reply_markup=inline_back)

#Режим карточки
@dp.callback_query_handler(lambda c: c.data == 'cards', state=Level_english.test)
async def error_cards(msg: types.CallbackQuery, state=FSMContext):
    await msg.answer('🛑 Ты уже прошел все слова. Пора перейти к тесту!😗')

@dp.callback_query_handler(lambda c: c.data == 'cards', state=[Level_english.mode_1, Level_english.mode_memory])
async def mode_cards(msg: types.CallbackQuery, state=FSMContext):
    with open(path_count_words, 'r+') as file_1:
        if f'{id_user[0]},{lvl_user[0]}' in str(file_1.readlines()):
            infa = count_words()
            await msg.answer('⛔ Подождите несколько секунд!')
            s = word_trans(infa)
            await msg.message.edit_text(f"Запомните эти слова😗\n{s}", reply_markup=inline_cards)
            await Level_english.mode_memory.set()
        else:
            await msg.answer('⛔ Подождите несколько секунд!')
            s = word_trans(15)
            await msg.message.edit_text(f"Запомните эти слова😗\n{s}", reply_markup=inline_cards)
            file_1.write(f'{id_user[0]},{lvl_user[0]},0:15\n')
            await Level_english.mode_memory.set()

# Режим заучивание
@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.test)
async def mode_error(msg: types.CallbackQuery, state=FSMContext):
    await msg.answer('🛑 Ты уже прошел все слова. Пора перейти к тесту!😗')

@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.mode_1)
async def mode_mem(msg: types.CallbackQuery, state=FSMContext):
    await msg.answer('🛑 Сначало пройди режим карточки!')

@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.mode_memory)
async def mode_memory(msg: types.CallbackQuery, state=FSMContext):
    k = word_text[0]
    correct_word.clear()
    correct_word.append(k)
    await msg.message.answer(f'{k}', reply_markup=create_question_memory(k))
    await msg.message.delete()
    word_text.remove(k)
    await Level_english.check_otvet.set()

@dp.message_handler(state=Level_english.check_otvet)
async def answer_check(msg: types.Message, state=FSMContext):
    num = randint(1,2)
    if len(word_text) > 0:
        for slovo in words_all:
            if f'{str(msg.text).capitalize()} - {correct_word[0].lower()}' == slovo:
                await msg.answer(f'{choice(answer_on_correct)}')
                break
        else:
            await msg.answer(f'{choice(answer_on_wrong)}')
            for gg in words_all:
                if correct_word[0] in gg:
                    await msg.answer(f'‼️{gg}‼️')
        k = word_text[0]
        correct_word.clear()
        correct_word.append(k)
        if num == 1:
            await msg.answer(f'{k}', reply_markup=create_question_memory(k))
        else:
            await msg.answer(f'✍️{k} - {"?"*5}', reply_markup=types.ReplyKeyboardRemove())
        word_text.remove(k)
    else:
        if msg.text.lower() == word_origin[-1]:
            await msg.answer('Правильно!')
        else:
            await msg.answer(f'{choice(answer_on_wrong)}')
            for gg in words_all:
                if word_origin[-1].capitalize() in gg:
                    await msg.answer(f'‼️{gg}‼️')
        await msg.answer('😊', reply_markup=types.ReplyKeyboardRemove())
        with open(path_levels, 'r') as file:
            d = file.readlines()
            for levl in d:
                levl = levl.strip('\n')
                if lvl_user[0] in levl:
                    await msg.answer('Молодец! Ты прошел режим заучивания этих 15 слов!', reply_markup=inline_back)
                    await Level_english.repeat.set()
                else:
                    await msg.answer('Молодец! Ты выучил все слова этого уровня!', reply_markup=inline_test)
                    await Level_english.test.set()

@dp.callback_query_handler(lambda c: c.data == 'test', state='*')
async def mode_test(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.answer('Красава')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)