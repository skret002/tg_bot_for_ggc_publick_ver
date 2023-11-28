import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from core.buttons.buttons import basic_menu
from core.buttons.buttons import generation_list_button as gn_but
from core.buttons.buttons import set_commands
from core.function.first_data import check_hash_code, get_email
from core.handlers import (apply_settings, day_night_settings, get_info,
                           new_user, notification, support)
from core.settings import settings
from core.states.new_user_state import StepNewUser
from core.utils.user_is_verified import user_is_verified
from logging_conf import logg

bot = Bot(settings.bot.token)
dp = Dispatcher(bot=bot)
dp.include_router(new_user.router)
dp.include_router(notification.router)
dp.include_router(apply_settings.router)
dp.include_router(day_night_settings.router)
dp.include_router(get_info.router)
dp.include_router(support.router)
@logg
async def cmd_start(message: types.Message):
    # sourcery skip: none-compare
    check_user = user_is_verified(message.chat.id)
    if check_user is None:
        await message.answer(
            f"Привет {message.from_user.full_name}! Я бот для управления системой SmartBox!,",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        menu = gn_but({"Да": "new_user", "Нет": "redirection_web"}, 2)
        await message.answer(
            "У вас уже есть регистрация на сайте ggc.center ?",
            reply_markup=menu.as_markup(),
        )
        dp.message.register(get_email, StepNewUser.GET_EMAIL)
        dp.message.register(check_hash_code, StepNewUser.GET_CODE)
    elif check_user is False:
        ...  # Такой юзер есть в БД но нет валидации по почте.
    else:
        await message.answer("Выберите действие", reply_markup=basic_menu)
dp.message(Command('main_menu'))
async def main_menu(message: types.Message,  state: FSMContext):
    await state.clear()
    await state.set_state()
    await message.answer("Выберите действие", reply_markup=basic_menu)

@logg
async def main():
    await set_commands(bot)
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(main_menu, Command('main_menu'))
    await dp.start_polling(bot, polling_timeout=10, max_delay=5.0)


if __name__ == "__main__":
    asyncio.run(main())
