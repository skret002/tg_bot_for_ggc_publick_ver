from aiogram.types import Message
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from core.states.new_user_state import NightModeState
from core.utils.fan_mode_kwargs import *
from core.buttons.buttons import generation_list_button as gn_bt
from core.utils.validation import str_to_int, check_hour
from core.utils.get_data_rigs import get_all_name_rigs
from core.models.model_func import prepare_write_dual_mode, dell_double_mod

router = Router()

@router.message(F.text == "Ночной режим")
async def temp_up_gpu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Что такое ночной режим, тут вы можете задать особые настройки для определенного времени.По сути у рига появятся вторичные настройки на которые он будет переключатся в указанное время. Сейчас соберем настройки, а потом можно будет применить их к нужным ригам."
    )
    menu = gn_bt(
        {"Создать новый": "create_night_mode", "Отключить": "inactiva_night_mode"}, 2
    )
    await message.answer(
        "Создать новый режим или отключить действующий?", reply_markup=menu.as_markup()
    )

@router.callback_query(F.data == "inactiva_night_mode")
async def not_accept_permission(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state()
    await callback.message.answer(
        "На каких ригах удалить?",
        reply_markup=gn_bt(get_all_name_rigs(callback.message.chat.id), 2).as_markup(),
    )
    await state.set_state(NightModeState.delete_mod)
    # дальше выбираем риги где нужно отключить.add()

@router.callback_query(NightModeState.delete_mod)
async def delete_mod(callback: types.CallbackQuery, state: FSMContext):
    dell_double_mod(callback.data)
    await callback.message.answer(f"Двойной режим удален для рига {callback.data}")

@router.callback_query(F.data == "create_night_mode")
async def accept_permission(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(active=True)
    select_mode_menu = gn_bt({"Автоматический": "0", "Статичный": "2"}, 2)
    await callback.message.answer(
        "Какой режим включать в указанное время",
        reply_markup=select_mode_menu.as_markup(),
    )
    await state.set_state(NightModeState.selected_mod)

@router.callback_query(NightModeState.selected_mod)
async def select_mode(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "2":
        await state.update_data(selected_mod=2)
        await callback.message.answer("Укажите скорость кулеров в % от 0 до 100")
        await state.set_state(NightModeState.static_set_rpm)
    else:
        await state.update_data(selected_mod=0)
        await callback.message.reply("Укажите температуру GPU")
        await state.set_state(NightModeState.terget_cpu)

@router.message(NightModeState.static_set_rpm)
async def set_static_set_rpm(message: Message, state: FSMContext):
    if str(str_to_int(message.text, 3)).isnumeric():
        await message.reply(f"Скорость кулеров принята {message.text}")
        await state.update_data(static_set_rpm=message.text)
        await message.answer(
            'Укажите время включения этих не очень хороших настроек в следующем формате "20:15"'
        )
        await state.set_state(NightModeState.time_start)
        # теперь выбор рига и запись в бд

@router.message(NightModeState.terget_cpu)
async def set_terget_cpu(message: Message, state: FSMContext):
    if str(str_to_int(message.text, 3)).isnumeric():
        await message.reply(f"Температура GPU {message.text} принята.")
        await state.update_data(
            terget_temp_min=int(message.text) - 5, terget_temp_max=int(message.text) + 5
        )
        await message.reply("Введите минимальный % внешним кулерам от 0 до 100")
        await state.set_state(NightModeState.min_fan_rpm)

@router.message(NightModeState.min_fan_rpm)
async def set_min_fan_rpm(message: Message, state: FSMContext):
    if str(str_to_int(message.text, 3)).isnumeric():
        await message.reply(f"Минимальная скорость  {message.text}% принята.")
        await state.update_data(min_fan_rpm=message.text)
        await message.reply("Укажите температуру MEM")
        await state.set_state(NightModeState.target_mem)

@router.message(NightModeState.target_mem)
async def set_target_mem(message: Message, state: FSMContext):
    if str(str_to_int(message.text, 3)).isnumeric():
        await message.reply(f"Температура MEM {message.text} принята.")
        await state.update_data(target_mem=message.text)
        await message.reply(
            "Укажите критическую температуру, она должна быть больше таргета GPU не менее, чем на 6 градусов."
        )
        await state.set_state(NightModeState.critical_temp)

@router.message(NightModeState.critical_temp)
async def set_critical_temp(message: Message, state: FSMContext):
    if str(str_to_int(message.text, 3)).isnumeric():
        await message.reply(f"{message.text} принята.")
        await state.update_data(critical_temp=message.text)
        await message.reply(
            'Укажите время включения этих не очень хороших настроек в следующем формате "20:15"'
        )
        await state.set_state(NightModeState.time_start)

@router.message(NightModeState.time_start)
async def set_time_start(message: Message, state: FSMContext):
    if check_hour(str(message.text)):
        await message.reply(f"Время старта {message.text} принято.")
        await state.update_data(time_start=message.text)
        await message.reply(
            "Укажите время завершения  этих настроек и возврат к предыдущем."
        )
        # await callback.message.reply('Вот и всё, а ты боялся :)')
        await state.set_state(NightModeState.time_end)
    else:
        await message.reply(f"{message.text} это не то, его я ожидал, повторите")

@router.message(NightModeState.time_end)
async def set_time_end(message: Message, state: FSMContext):
    if check_hour(str(message.text)):
        await message.reply(f"Время окончания  {message.text} принято.")
        await state.update_data(time_end=message.text)
        await message.answer("Вот и всё, а ты боялся :)")
        await message.answer(
            "Для каких ригов применить?",
            reply_markup=gn_bt(get_all_name_rigs(message.chat.id), 2).as_markup(),
        )
        await state.set_state(NightModeState.rig_id)
        # Теперь выбор рига и запись
    else:
        await message.reply(f"{message.text} это не то, его я ожидал, повторите")

@router.callback_query(NightModeState.rig_id)
async def select_rigs(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["selected_mod"] == 0 and data["active"] is True:
        prepare_write_dual_mode(
            selected_mod=0,
            terget_temp_min=data["terget_temp_min"],
            terget_temp_max=data["terget_temp_max"],
            min_fan_rpm=data["min_fan_rpm"],
            target_mem=data["target_mem"],
            critical_temp=data["critical_temp"],
            time_start=data["time_start"],
            time_end=data["time_end"],
            rig_id=callback.data,
            id_tg=callback.message.chat.id,
            active=True,
        )

    elif data["selected_mod"] == 2 and data["active"] is True:
        prepare_write_dual_mode(
            selected_mod=2,
            static_set_rpm=data["static_set_rpm"],
            time_start=data["time_start"],
            time_end=data["time_end"],
            rig_id=callback.data,
            id_tg=callback.message.chat.id,
            active=True,
        )
    await callback.message.answer(f"Двойной режим создан для рига {callback.data}")
