from aiogram.types import Message
from aiogram import F, Router,types
from aiogram.fsm.context import FSMContext
from core.states.new_user_state import SettingsState
from core.utils.fan_mode_kwargs import *
from core.buttons.buttons import settings_menu
from core.buttons.buttons import generation_list_button as gn_bt,basic_menu
from core.utils.validation import str_to_int,ERROR_RESPONSES
from core.utils.get_data_rigs import get_all_name_rigs
from core.utils.common_apply_settings import prepare_settings,correspondence,correspondence_message
from core.utils.make_request import make_request 
router = Router()

@router.callback_query(SettingsState.select_rigs)
async def select_rigs_and_write(callback: types.CallbackQuery, state: FSMContext):
    # sourcery skip: remove-redundant-if
    data = await state.get_data()
    try:
        ready_data=prepare_settings(callback.data,callback.message.chat.id,data['settings'])
        make_request(prefix='set_option_rig_from_bot/',param=ready_data,method='POST')
        await callback.message.answer(f"Выполнено {list(data['settings'])[0]} {data['settings'][list(data['settings'])[0]]}")
    except TypeError:
        await callback.message.answer("Ууупс, с этим ригом что то пошло не так. Мне не хватает данных с сервера. Но можно выбрать другой риг")

async def get_permission_change_mod(message: Message,state: FSMContext):
    menu=gn_bt({'Да':'permission_change_mod','Нет':'not_permission_change_mod'},2)
    await message.answer("Внимание, если на ваших ригах вкдючен режим 'Управление из Hive', необходимо изменить данную настройку на 'Управление с сайта'! Вы разрешаете выполнить это автоматически?", reply_markup=menu.as_markup())
    await state.set_state(SettingsState.get_permission)
@router.callback_query(F.data == "permission_change_mod")
async def response_permission(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Что хотите изменить?", reply_markup=settings_menu)
@router.callback_query(F.data == "not_permission_change_mod") 
async def not_accept_permission(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state()
    await callback.message.answer("Тогда я не смогу изменить параметры. Но вы можете сделать это на сайте ggc.center или в вашей OS", reply_markup=basic_menu)
    
@router.message(F.text == "Выполнить действие с ригом")
async def permission_request(message: Message,state: FSMContext):
    await state.clear()
    await get_permission_change_mod(message,state)

@router.message(F.text == "Установить GPU Temp")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите температуру для GPU:")
    await state.update_data(settings='gpu',len_test=2)
    await state.set_state(SettingsState.gpu_temp)

@router.message(F.text == "Установить Mem Temp")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите температуру для MEM:")
    await state.update_data(settings='mem',len_test=2)
    await state.set_state(SettingsState.mem_temp)

@router.message(F.text == "Минимальный Fan")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите минимальный % для кулеров")
    await state.update_data(settings='min_fan',len_test=3)
    await state.set_state(SettingsState.min_fan)
@router.message(F.text == "Критическая")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите температуру, при которой мы будем панически использовать весь арсенал для охлаждения, включая остановку майнера!")
    await state.update_data(settings='critical',len_test=3)
    await state.set_state(SettingsState.critical)

@router.message(F.text == "Изменить режим")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите 0 для установки режима 'Авто' или 2 для 'Статического'")
    await state.update_data(settings='selected_mod',len_test=1)
    await state.set_state(SettingsState.change_mod)
@router.message(F.text == "Изменить статичный %")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Для установки скорости в статичном режиме, введите % от 0 до 100")
    await state.update_data(settings='SetRpm',len_test=3)
    await state.set_state(SettingsState.static_rpm)
    
@router.message(SettingsState.static_rpm)
@router.message(SettingsState.change_mod)
@router.message(SettingsState.min_fan)
@router.message(SettingsState.critical)
@router.message(SettingsState.mem_temp)
@router.message(SettingsState.gpu_temp)
async def get_temp_val(message: Message,state: FSMContext):
    data = await state.get_data()
    param=correspondence[data['settings']]
    mess=correspondence_message[data['settings']]
    await message.reply("проверяю ...")
    await message.reply(f"{mess} message.text")
    print(str_to_int(message.text,data['len_test']))
    if str(str_to_int(message.text,data['len_test'])).isnumeric():
        await state.update_data(settings={param:message.text})
        await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())
        await state.set_state(SettingsState.select_rigs)
        # Теперь записать в бд
    else:
        await message.reply(f"{ERROR_RESPONSES['str_not_int']}")

