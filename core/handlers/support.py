from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from core.states.new_user_state import SupportState
from core.models.model_func import add_question, get_filter_id_tg
router = Router()


@router.message(F.text == "Обратиться в техподдержку")
async def first_q_support(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Описывая проблему, сформурируйте ее четко и коротко. Обязательно напишите с каким именно ригом у вас проблема указав его id в строгом формате, пример ID-390124. Если сообщение будет достойное, я прослежу, что бы разработчик его увидел."
        "Ожидаю сообщение ..."
    )
    await state.set_state(SupportState.await_mess)


@router.message(SupportState.await_mess)
async def get_mess(message: Message):
    if "ID" in message.text:
        for word in str(message.text).split(" "):
            if "ID" in word:
                rig_id = word.split("-")[-1]
    else:
        rig_id = "Нет"
    if len(message.text) > 20:
        user = get_filter_id_tg(message.chat.id)
        add_question(user_id=user.id, question=message.text, id_rig=rig_id)
        await message.answer("Ваше сообщение принято и отправлено куда следует.")
    else:
        await message.answer("Ваше сообщение не содержит ничего полезного")
