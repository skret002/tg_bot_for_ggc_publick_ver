import time
from aiogram.types import Message
from aiogram import F,Router,types
from aiogram.fsm.context import FSMContext
from core.states.new_user_state import NotificationMenuClass,SelectRigsClass
from core.utils.validation import str_to_int,ERROR_RESPONSES
from core.utils.get_data_rigs import get_all_name_rigs
from core.buttons.buttons import notification_menu
from core.buttons.buttons import generation_list_button as gn_bt,basic_menu
from core.models.model_func import add_notification,dell_notification_id
router = Router()

def test_to_bool(name_arg: str, value: int) -> bool or None:
    # sourcery skip: lift-duplicated-conditional
    list_args=['if_off']
    if  name_arg in list_args and value >= 1:
        return True
    elif name_arg in list_args and value == 0:
        return False
    return None


@router.callback_query(SelectRigsClass.select_rigs)
async def select_rigs_and_write(callback: types.CallbackQuery, state: FSMContext):
    # sourcery skip: remove-redundant-if
    data = await state.get_data()
    print(" data['notes']",data['notes'] == 'delete')
    if data['notes'] == 'delete':
        dell_notification_id(callback.data)
        await callback.message.reply(f'Слежение отключено для  рига ID={callback.data}')
    else:
        param=list(data['notes'])[0] #'if_hot_gpu'
        if data['notes'][param] !=0:
            await callback.message.reply(f'Теперь слежу за ригом ID={callback.data}')
        elif data['notes'][param] ==0:
            await callback.message.reply(f'Больше не слежу за ригом ID={callback.data}')
        tg_user_id = callback.message.chat.id
        tb=test_to_bool(param,int(data['notes'][param]))
        if tb != None:
            data['notes'][param] = tb
        add_notification(id_tg=tg_user_id,dop_args={param:data['notes'][param]}, rig_id=callback.data)

@router.message(F.text == "Настроить оповещения")
async def new_user_get_data(message: Message,state: FSMContext):
    await message.answer("Выберите параметр", reply_markup=notification_menu)


@router.message(F.text == "Температура GPU выше")
async def temp_up_gpu(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение, при привышении которого, желаете получать уведомление или установите 0 для отключения уведомления", reply_markup=notification_menu)
    await state.set_state(NotificationMenuClass.GPU_TEMP)
@router.message(NotificationMenuClass.GPU_TEMP)
async def get_temp_val(message: Message,state: FSMContext):
    await message.reply("проверяю ...")
    if str_to_int(message.text,3) != False:
        await message.answer(f"Значение принято, если t-gpu > {message.text}")
        await state.update_data(notes={'if_hot_gpu':message.text})
        await state.set_state(SelectRigsClass.select_rigs)
        await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())
        # Теперь записать в бд
    else:
        await message.reply(f"{ERROR_RESPONSES['str_not_int']}")

@router.message(F.text == "Температура MEM выше")
async def if_temp_up(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение, при привышении которого, желаете получать уведомление или установите 0 для отключения уведомления", reply_markup=notification_menu)
    await state.set_state(NotificationMenuClass.GPU_MEM)
@router.message(NotificationMenuClass.GPU_MEM)
async def get_temp_value(message: Message,state: FSMContext):
    await message.reply("проверяю ...")
    if str_to_int(message.text,3) != False:
        await message.answer(f"Значение принято, если t-mem > {message.text}")
        await state.update_data(notes={'if_hot_mem':message.text})
        await state.set_state(SelectRigsClass.select_rigs)
        await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())
        # Теперь записать в бд
    else:
        await message.reply(f"{ERROR_RESPONSES['str_not_int']}")
@router.message(F.text == "RPM кулера выше")
async def if_rpm_up(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение, при привышении которого, желаете получать уведомление или установите 0 для отключения уведомления", reply_markup=notification_menu)
    await state.set_state(NotificationMenuClass.RPM_FAN)
@router.message(NotificationMenuClass.RPM_FAN)
async def get_rpm_value(message: Message,state: FSMContext):
    await message.reply("проверяю ...")
    if str_to_int(message.text,6) != False:
        await message.answer(f"Значение принято, если скорость внешних кулеров > {message.text}")
        await state.update_data(notes={'if_fan_rpm':message.text})
        await state.set_state(SelectRigsClass.select_rigs)
        await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())
        # Теперь записать в бд
    else:
        await message.reply(f"{ERROR_RESPONSES['str_not_int']}")

@router.message(F.text == "Риг недоступен")
async def if_offline(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение 1 для отслеживание или 0 для отключения", reply_markup=notification_menu)
    await message.reply("проверяю ...")
    await state.set_state(NotificationMenuClass.ON_OFF)
@router.message(NotificationMenuClass.ON_OFF)
async def get_rpm_value(message: Message,state: FSMContext):
    await message.answer("Значение принято, если будет недоступен, сообщу.")
    await state.update_data(notes={'if_off':message.text})
    await state.set_state(SelectRigsClass.select_rigs)
    await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())
@router.message(F.text == "Внешние кулера 0 rpm")
async def if_fan_stop(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение 1 для отслеживание или 0 для отключения", reply_markup=notification_menu)
    await message.reply("проверяю ...")
    await state.set_state(NotificationMenuClass.FAN_ZERO)
@router.message(NotificationMenuClass.FAN_ZERO)
async def get_rpm_value(message: Message,state: FSMContext):
    await message.answer("Значение принято, если будет недоступен, сообщу.")
    await state.update_data(notes={'if_fan_rpm_zero':message.text})
    await state.set_state(SelectRigsClass.select_rigs)
    await message.answer('Для каких ригов применить?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())

@router.message(F.text == "Отключить слежение")
async def get_rpm_value(message: Message,state: FSMContext):
    await state.update_data(notes='delete')
    await state.set_state(SelectRigsClass.select_rigs)
    await message.answer('На каких ригах отключаем?',reply_markup=gn_bt(get_all_name_rigs(message.chat.id),2).as_markup())

@router.message(F.text == "Хешрейт ниже")
async def if_hash_low(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Введите значение, ниже которого, желаете получать уведомление", reply_markup=notification_menu)
    await state.set_state(NotificationMenuClass.HASH_LOW)
@router.message(NotificationMenuClass.HASH_LOW)
async def get_hash_value(message: Message,state: FSMContext):
    await message.reply("проверяю ...")
    if str_to_int(message.text,10) != False:
        #await message.answer(f"Значение принято, если хэш hashrate меньше {message.text}")
        await message.answer("Данная функция еще не реализованна, мы сообщим когда запустим ее!")
        # этой функции пока нет в софте
    else:
        await message.reply(f"{ERROR_RESPONSES['str_not_int']}")

@router.message(F.text == "Кормить кота")
async def feed_at(message: Message,state: FSMContext):
    await state.clear()
    await message.answer("Если я через 5 мин не услышу мурчание довольного кота, ригам вашим хана. Тик-Так", reply_markup=notification_menu)
    for i in range(300):
        time_off=300 - i
        await message.answer(f"осталось {time_off} сек. Я жду запись звука:)", reply_markup=notification_menu)
        time.sleep(1)
    await message.answer("Ахахаха, а чего ты ожидал от этой функции в майнинг боте))) конечно же это смеха ради! Хорошего вам настроения.", reply_markup=notification_menu)

@router.message(F.text == "Главное меню")
async def feed_at(message: Message,state: FSMContext):
    await state.set_state()
    await message.answer("Выберите действие", reply_markup=basic_menu)