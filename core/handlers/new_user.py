from aiogram import F,Router,types
from aiogram.fsm.context import FSMContext
from core.states.new_user_state import StepNewUser
router = Router()

@router.callback_query(F.data == "new_user")
async def new_user_get_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите адрес почты, указанный ранее на ggc.center')
    await state.set_state(StepNewUser.GET_EMAIL)

@router.callback_query(F.data == "redirection_web")
async def redirection_web(callback: types.CallbackQuery):
    await callback.message.answer('Извините, сначала нужно выполнить инструкцию http://ggc.center/#/instruction \n После обязательно возвращайтесь.')  