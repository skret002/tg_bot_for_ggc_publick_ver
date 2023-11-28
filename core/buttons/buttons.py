from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import types,Bot
from click import command

builder = InlineKeyboardBuilder()
async def set_commands(bot:Bot):
    commands=[
        BotCommand(
            command='start',
            description='Запустить бот'
        ),
        BotCommand(
            command='main_menu',
            description='Главное меню'
        )
    ]
    await bot.set_my_commands(commands,BotCommandScopeDefault())

change_mod_menu = settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Авто режим")],
        [KeyboardButton(text="Статичный режим")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
night_mode_menu = settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вкл night mode")],
        [KeyboardButton(text="Выкл night mode")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Установить GPU Temp")],
        [KeyboardButton(text="Установить Mem Temp")],
        [KeyboardButton(text="Минимальный Fan")],
        [KeyboardButton(text="Критическая")],
        [KeyboardButton(text="Изменить статичный %")],
        [KeyboardButton(text="Изменить режим")],
        [KeyboardButton(text="Ночной режим")],
        [KeyboardButton(text="Главное меню")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def generation_list_button(dict_but, count_rou=1):
    print("dict_but", dict_but)
    builder = InlineKeyboardBuilder()
    for i in dict_but:
        # builder.button(text=i, callback_data=dict_but[i])
        builder.add(types.InlineKeyboardButton(text=i, callback_data=dict_but[i]))
    builder.adjust(count_rou)
    return builder


basic_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Настроить оповещения")],
        [KeyboardButton(text="Выполнить действие с ригом")],
        [KeyboardButton(text="Получить сводные данные")],
        [KeyboardButton(text="Обратиться в техподдержку")],
        [KeyboardButton(text="Главное меню")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
notification_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Температура GPU выше")],
        [KeyboardButton(text="Температура MEM выше")],
        [KeyboardButton(text="RPM кулера выше")],
        [KeyboardButton(text="Риг недоступен")],
        [KeyboardButton(text="Внешние кулера 0 rpm")],
        [KeyboardButton(text="Хешрейт ниже")],
        [KeyboardButton(text="Отключить слежение")],
        [KeyboardButton(text="Кормить кота")],
        [KeyboardButton(text="Главное меню")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

change_settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Изменить таргет GPU")],
        [KeyboardButton(text="Изменить таргет MEM")],
        [KeyboardButton(text="Установить статичный")],
        [KeyboardButton(text="Задать ручной диапазон")],
        [KeyboardButton(text="Отключить GPU")],
        [KeyboardButton(text="Ночной режим")],
        [KeyboardButton(text="Применить настройки")],
        [KeyboardButton(text="Главное меню")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)
