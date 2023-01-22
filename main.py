import os
import json
from random import*
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from decouple import config
from googletrans import Translator
from keyboards import inline_keyboard, inline_mode, choice_md, inline_back, inline_levels, inline_cards, inline_test, inline_menu

TOKEN = config('API_TOKEN')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

path_accounts = 'accounts.json'
path_levels = 'levels.json'
path_description = 'description.txt'
path_info = 'levels_english'
path_count_words = 'count_words.json'
path_translate = 'translate.json'
answer_on_correct = ['Молодец😊', 'Так держать😙', 'Я тобой горжусь😊', 'Неплохо😏', 'Отлично😊']
answer_on_wrong = ['Ты немного ошибся😶', 'Нет😥', 'Ну нет же🙄', 'Неа😥', 'Ты ошибся🤔']

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
    test_otvet = State()

def check_lvl(data, id):
    with open(path_levels, 'r') as file:
        try:
            content = json.load(file)
            if id in content.keys():
                if data in content[id]:
                    return False
                else:
                    return True
            else:
                return True
        except:
            return True
        
def lvl(id):
    lvl_keyboard = types.InlineKeyboardMarkup()
    with open(path_levels, 'r') as file:
        try:
            content = json.load(file)
            for i in content[id]:
                lvl_keyboard.add(types.InlineKeyboardButton(i, callback_data=i))
            lvl_keyboard.add(types.InlineKeyboardButton('Back👈', callback_data='back'))
        except:
            lvl_keyboard.add(types.InlineKeyboardButton('Back👈', callback_data='back'))
    return lvl_keyboard

def translate_word(words):
    words_all = []
    word_origin = []
    word_text = []
    translator = Translator()
    translations = translator.translate(text=words, src='en', dest='ru')
    for translation in translations:
        word_origin.append(translation.origin.lower())
        word_text.append(translation.text.lower())
        words_all.append(f'{translation.origin.capitalize()} - {translation.text.lower()}')
    return words_all, word_origin, word_text
    
def word_trans(index, lvl_user):
    info = os.listdir(path_info)
    for i in info:
        if f'{lvl_user}.txt' in i:
            with open(rf'{path_info}\{i}', 'r') as file_2:
                dat = file_2.readline().split(',')
                content = ''
                if type(index) == int:
                    g = translate_word(dat[:index])
                    for el in g[0]:
                        content += f'{el}\n'
                else:
                    g = translate_word(dat[int(index[0]):int(index[1])])
                    for el in g[0]:
                        content += f'{el}\n'
                return content, g[0], g[1], g[2]

def count_words(infa, id, lvl_user):
    with open(path_count_words, 'w') as file_2:
        info = infa[id][0][lvl_user]
        tt = []
        for i in info.split(':'):
            tt.append(str(int(i)+15))
        tt_1 = ':'.join(tt)
        if int(tt[1]) >= 105:
            with open(path_levels, 'r') as file_3:
                content_1 = json.load(file_3)
            with open(path_levels, 'w') as file_4:
                content_1[id].remove(lvl_user)
                file_4.write(json.dumps(content_1))
                infa[id][0].pop(lvl_user)
        else:
            infa[id][0][f"{lvl_user}"] = tt_1
        file_2.write(json.dumps(infa))
        return tt

def create_question_memory(word, word_origin, words_all):
        keyboard = types.ReplyKeyboardMarkup()
        word_origin_1 = word_origin[:]
        f = []
        buttons = []
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
    await msg.answer('Привет! Я бот для изучения английской лексики по разным уровням.', reply_markup=types.ReplyKeyboardRemove())
    await msg.answer('Для начала войди в аккаунт или зарегистрируйся!', reply_markup=inline_keyboard)

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

@dp.callback_query_handler(lambda c: c.data == 'menu', state=Level_english.test_otvet)
async def back_menu(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text('Выберите что вас интересует!', reply_markup=choice_md)
    await Level_english.choice.set()

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

@dp.message_handler(state=Register.register_account)
async def create_account(msg: types.Message, state=FSMContext):
    with open(path_accounts, 'r+') as file:
        try:
            content = json.load(file)
            for key in content.keys():
                if key == str(msg.from_id):
                    await msg.answer("Извините на этом устройстве уже есть аккаунт🤨. Попробуйте ввойти в него!", reply_markup=inline_back)
                    await state.finish()
                    break
            else:
                async with state.proxy() as data:
                    data['id'] = str(msg.from_id)
                with open(path_accounts, 'w') as file_1:
                    content[f'{msg.from_id}'] = f'{msg.text.lower()}'
                    json.dump(content, file_1)
                    await msg.answer("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
                    await Level_english.choice_lvl.set()
        except:
                async with state.proxy() as data:
                    data['id'] = str(msg.from_id)
                a = {f'{msg.from_id}': f'{msg.text.lower()}'}
                json.dump(a, file)
                await msg.answer("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
                await Level_english.choice_lvl.set()
            
@dp.callback_query_handler(lambda c: c.data == 'enter', state='*')
async def enter_account(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.edit_text("Введите свой ник для аккаунта!")
    await Register.enter.set()
    
@dp.message_handler(state=Register.enter)
async def account(msg: types.Message, state=FSMContext):
    with open(path_accounts, 'r+') as file:
        try:
            content = json.load(file)
            for key, value in content.items():
                if key == str(msg.from_id) and value == msg.text.lower():
                    await msg.answer(f'Вы успешно вошли в ваш аккаунт, {msg.text}!', reply_markup=choice_md)
                    async with state.proxy() as data:
                        data['id'] = str(msg.from_id)
                    await Level_english.choice.set()
                    break
            else:
                await msg.answer(f'Такого ника нет в нашей базе данных🤨. Вернитесь на главное меню!', reply_markup=inline_back)
                await state.finish()
        except:
            await msg.answer(f'Такого ника нет в нашей базе данных🤨. Вернитесь на главное меню!', reply_markup=inline_back)
            await Register.enter.set()

# Выбор уровня английского при первой регистрации или проверка уровня при входе
@dp.callback_query_handler(state=Level_english.choice_lvl)
async def level_choice(msg: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        id_user = data['id']
        data['lvl'] = str(msg.data)
    if check_lvl(msg.data, id_user) == True:
        with open(path_levels, 'r+') as file_1:
            try:
                content = json.load(file_1)
                with open(path_levels, 'w') as file_2:
                    if id_user in content.keys():
                        content[id_user].append(f'{msg.data}')
                        file_2.write(json.dumps(content))
                    else:
                        content[id_user] = [f'{msg.data}']
                        file_2.write(json.dumps(content))
            except:
                dict_lvl = {}
                dict_lvl[id_user] = [f'{msg.data}']
                file_1.write(json.dumps(dict_lvl))
        await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)
        await Level_english.mode_1.set()
    else:
        await msg.message.edit_text('Извините, вы уже выбирали этот уровень английского! Выберите что вас интересует!😉', reply_markup=choice_md)
        await Level_english.choice.set()

@dp.callback_query_handler(state=Level_english.choice)
async def level_choice(msg: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        id_user = data['id']
    if msg.data == 'new':
        await msg.message.edit_text("Выберите уровень английского, который хотите изучать!🇬🇧", reply_markup=inline_levels)
        await Level_english.choice_lvl.set()
    else:
        await msg.message.edit_text("Выберите уровень английского, который продолжишь изучать!🇬🇧", reply_markup=lvl(id_user))
        await Level_english.mode_2.set()

@dp.callback_query_handler(state=Level_english.mode_2)
async def enter_mode(msg: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        data['lvl'] = str(msg.data)
    await msg.message.edit_text('Теперь выбери режим изучения!🤗', reply_markup=inline_mode)
    await Level_english.mode_1.set()

# #Выбор режима изучения
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
    async with state.proxy() as data:
        id_user = data['id']
        lvl_user = data['lvl']
        with open(path_count_words, 'r+') as file_1:
            try:
                content = json.load(file_1)
                with open(path_count_words, 'w') as file_2:
                    if id_user in content.keys() and lvl_user in content[id_user][0].keys():
                            infa = count_words(content, id_user, lvl_user)
                            await msg.answer('⛔ Подождите несколько секунд!')
                            s = word_trans(infa, lvl_user)
                            await msg.message.edit_text(f"Запомните эти слова😗\n{s[0]}", reply_markup=inline_cards)
                            await Level_english.mode_memory.set()
                    else:
                        await msg.answer('⛔ Подождите несколько секунд!')
                        s = word_trans(15, lvl_user)
                        await msg.message.edit_text(f"Запомните эти слова😗\n{s[0]}", reply_markup=inline_cards)
                        if id_user in content.keys():
                            content[id_user][0][f"{lvl_user}"] = "0:15"
                        else:
                            content[id_user] = [{lvl_user: '0:15'}]
                        file_2.write(json.dumps(content))
                        await Level_english.mode_memory.set()
            except:
                await msg.answer('⛔ Подождите несколько секунд!')
                s = word_trans(15, lvl_user)
                await msg.message.edit_text(f"Запомните эти слова😗\n{s[0]}", reply_markup=inline_cards)
                dict_word = {}
                dict_word[id_user] = [{lvl_user: '0:15'}]
                file_1.write(json.dumps(dict_word))
                await Level_english.mode_memory.set()
        data['words_all'] = s[1]
        data['word_origin'] = s[2]
        data['word_text'] = s[3]

# Режим заучивание
@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.test)
async def mode_error(msg: types.CallbackQuery, state=FSMContext):
    await msg.answer('🛑 Ты уже прошел все слова. Пора перейти к тесту!😗')

@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.mode_1)
async def mode_mem(msg: types.CallbackQuery, state=FSMContext):
    await msg.answer('🛑 Сначала пройди режим карточки!')

@dp.callback_query_handler(lambda c: c.data == 'memorization', state=Level_english.mode_memory)
async def mode_memory(msg: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        word_text = data['word_text']
        word_origin = data['word_origin']
        words_all = data['words_all']
        k = word_text[0]
        data['correct_word'] = k
        await msg.message.answer(f'{k}', reply_markup=create_question_memory(k, word_origin, words_all))
        await msg.message.delete()
        word_text.remove(k)
        data['word_text'] = word_text
        await Level_english.check_otvet.set()

@dp.message_handler(state=Level_english.check_otvet)
async def answer_check(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        id_user = data['id']
        lvl_user = data['lvl']
        correct_word = data['correct_word']
        word_text = data['word_text']
        word_origin = data['word_origin']
        words_all = data['words_all']
    num = randint(1,2)
    if len(word_text) > 0:
        for slovo in words_all:
            if f'{str(msg.text).capitalize()} - {correct_word.lower()}' == slovo:
                await msg.answer(f'{choice(answer_on_correct)}')
                break
        else:
            await msg.answer(f'{choice(answer_on_wrong)}')
            for gg in words_all:
                if correct_word in gg:
                    await msg.answer(f'‼️{gg}‼️')
        k = word_text[0]
        async with state.proxy() as data:
            data['correct_word'] = k
            if num == 1:
                await msg.answer(f'{k}', reply_markup=create_question_memory(k, word_origin, words_all))
            else:
                await msg.answer(f'✍️{k} - {"?"*5}', reply_markup=types.ReplyKeyboardRemove())
            word_text.remove(k)
            data['word_text'] = word_text
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
            content = json.load(file)
            if lvl_user in content[id_user]:
                await msg.answer('Молодец! Ты прошел режим заучивания этих 15 слов!', reply_markup=inline_back)
                await Level_english.repeat.set()
            else:
                await msg.answer('Молодец! Ты выучил все слова этого уровня!', reply_markup=inline_test)
                await Level_english.test.set()

#Режим тест
@dp.callback_query_handler(lambda c: c.data == 'test', state='*')
async def mode_test(msg: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        lvl_user = data['lvl']
        with open(path_translate, 'r') as file:
            content = json.load(file)
        key = list(content[lvl_user].keys())
        await msg.message.edit_text(f'✍️{key[0]} - {"?"*5}')
        data['keys'] = key
        data['correct'] = 0
        data['wrong'] = 0
        data['all'] = 1
    await Level_english.test_otvet.set() 
                  
@dp.message_handler(state=Level_english.test_otvet)
async def test_answer_check(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        id_user = data['id']
        keys = data['keys']
        lvl_user = data['lvl']
        with open(path_translate, 'r') as file:
            content = json.load(file)
            if content[lvl_user][keys[0]] == msg.text.lower():
                data['correct'] += 1
                await msg.answer(f'{choice(answer_on_correct)}')
            else:
                data['wrong'] += 1
                await msg.answer(f'{choice(answer_on_wrong)}')
            keys.pop(0)
            data['keys'] = keys
            if len(keys) > 0:
                await msg.answer(f'✍️{keys[0]} - {"?"*5}')
                data['all'] += 1
            else:
                await msg.answer(f'Молодец! Ты прошел тест!😊\n<b>Всего вопросов:</b> {data["all"]}\n<b>Количество правильных ответов:</b> {data["correct"]}\n<b>Количество неправильных ответов:</b> {data["wrong"]}', parse_mode='HTML')
                if data['correct'] > data['wrong']:
                    await msg.answer('Молодец! Ты хорошо выучил слова этого уровня!😗', reply_markup=inline_menu)
                else:
                    await msg.answer('Твои результаты не очень хорошие😢\nПопробуй снова выучить слова этого уровня!', reply_markup=inline_menu)
                with open(path_levels, 'r') as file_1:
                    content_1 = json.load(file_1)
                with open(path_levels, 'w') as file_2:
                    content_1[id_user].remove(lvl_user)
                    file_2.write(json.dumps(content_1))
                try:
                    with open(path_count_words, 'r+') as file_3:
                        content = json.load(file_3)
                        content[id_user][0].pop(lvl_user)
                        with open(path_count_words, 'w') as file_4:
                            file_4.write(json.dumps(content))
                except:
                    pass
    await state.finish()

@dp.message_handler(state='*')
async def bot_otvet(msg: types.Message):
    await msg.answer('Не знаешь что сделать?\n/start')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)