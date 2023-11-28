from aiogram.fsm.context import FSMContext
from core.states.new_user_state import StepNewUser
from aiogram.types import Message
from core.utils.validation import mail_validate
from core.utils.make_request import make_request
from core.models.model_func import add_user
from core.buttons.buttons import basic_menu
import hashlib
from logging_conf import logg

def get_hash(chat_id: str, user_name: str, first_name: str) -> int:
    h = chat_id + user_name + first_name
    return hashlib.md5(h.encode("utf-8")).hexdigest()


async def get_email(message: Message, state: FSMContext):
    HASH = get_hash(
        str(message.chat.id),
        str(message.from_user.username),
        str(message.from_user.first_name),
    )
    await message.answer("Введите адрес почты, указанный ранее на ggc.center")
    await state.update_data(email=message.text)
    mail = mail_validate(message.text)
    if mail["status"] is False:
        await message.reply(mail["text"])
    else:
        req_user = make_request(
            prefix="mail_for_bot/",
            param={"hash": HASH, "email": mail["text"]},
            method="POST",
        )
        if "Done" in req_user["data"]["status"]:
            await message.answer(
                "На ваш email отправлен проверочный код, введите его..."
            )
            await state.update_data(user_info=req_user["data"])
            await state.set_state(StepNewUser.GET_CODE)
        else:
            await message.answer(
                f'Ваш email {mail["text"]} не обнаружен в базе ggc.center'
            )


async def check_hash_code(message: Message, state: FSMContext):
    user_data_in_state = await state.get_data()
    HASH = get_hash(
        str(message.chat.id),
        str(message.from_user.username),
        str(message.from_user.first_name),
    )
    if str(message.text) == HASH:
        add_user(
            name=user_data_in_state["user_info"]["user_name"],
            utc=user_data_in_state["user_info"]["time_offset"],
            mail=user_data_in_state["email"],
            id_tg=message.from_user.id,
            id_server=user_data_in_state["user_info"]["user_id"],
            hash_user=HASH,
            valid=True,
        )  # записываем юзера в бд
        await message.answer("Аккаунт создан, можно пользоваться.")
        await state.clear()
        await message.answer("Выберите действие", reply_markup=basic_menu)
    else:
        await message.reply("Этот код не верный.Жду правильный код!")
