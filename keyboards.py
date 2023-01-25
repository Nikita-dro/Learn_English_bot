from aiogram import types

inline_back = types.InlineKeyboardMarkup()
inline_back.add(types.InlineKeyboardButton('Back👈', callback_data='back'))

inline_menu = types.InlineKeyboardMarkup()
inline_menu.add(types.InlineKeyboardButton('Меню💻', callback_data='menu'))

test_menu = types.ReplyKeyboardMarkup()
test_menu.add(types.KeyboardButton('Продолжить позже😙'))

inline_start = types.InlineKeyboardMarkup()
inline_start.add(types.InlineKeyboardButton('Начать тест', callback_data='new'))

choice_test = types.InlineKeyboardMarkup(row_width=1)
m_1 = types.InlineKeyboardButton('Начать тест', callback_data='new')
m_2 = types.InlineKeyboardButton('Продолжить тест этого уровня😌', callback_data='old')
choice_test.add(m_1, m_2)

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