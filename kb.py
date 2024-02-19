from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="🖼 Генерировать изображение", callback_data="generate_image")],
    [InlineKeyboardButton(text="💰 Баланс", callback_data="balance")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")],
]
room_types = [
    [InlineKeyboardButton(text="Спальня", callback_data="bedroom"),
     InlineKeyboardButton(text="Гостиная", callback_data="living room")],
    [InlineKeyboardButton(text="Кухня", callback_data="kitchen"),
     InlineKeyboardButton(text="Ванная", callback_data="bathroom")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]
room_styles = [
    [InlineKeyboardButton(text="Модерн", callback_data="modern"),
    InlineKeyboardButton(text="Минимализм", callback_data="minimalism"),
     InlineKeyboardButton(text="Японский", callback_data="japanese")],
    [InlineKeyboardButton(text="Дзен", callback_data="zen"),
    InlineKeyboardButton(text="Скандинавский", callback_data="scandinavian"),
     InlineKeyboardButton(text="Деревенский", callback_data="country")],
    [InlineKeyboardButton(text="Винтаж", callback_data="vintage"),
    InlineKeyboardButton(text="Тропический", callback_data="tropical"),
     InlineKeyboardButton(text="Прибрежный", callback_data="coastal")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
room_types = InlineKeyboardMarkup(inline_keyboard=room_types)
room_styles = InlineKeyboardMarkup(inline_keyboard=room_styles)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])