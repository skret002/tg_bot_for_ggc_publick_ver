from aiogram.types import Message
from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from core.utils.common_get_info import get_all_rigs_status
router = Router()

mod_option_hive_mess={'0':'Управляется c сайта', '1':'Управляется из ОС'}
alertFan_mess={'False':'Ошибок по кулерам Gpu не найдено или не отслеживается','True':'Есть ошибка по кулеру на Gpu'}
selected_mod_mess={'0':'Режим Авто','1':'Ручные настройки','2':'Статичный режим'}
rig_online_status_mess={'False':'Выключен','True':'Включен'}

@router.message(F.text == "Получить сводные данные")
async def new_user_get_data(message: Message,state: FSMContext):
    await message.answer("Формирую данные, это займет пару мгновений...")
    all_data=get_all_rigs_status(message.chat.id)
    for item in all_data:
        rig_name=item['rigName']
        rigId=item['rigId']
        mod_option_hive=mod_option_hive_mess[str(item['mod_option_hive'])]
        AlertFan=alertFan_mess[str(item['AlertFan']['alertFan'])]
        number_gpu_alert=item['AlertFan']['numberGpu']
        selected_mod=selected_mod_mess[str(item['SetModeFan']['selected_mod'])]
        terget_temp_min=item['SetMode0']['terget_temp_min']
        terget_temp_max=item['SetMode0']['terget_temp_max']
        target_mem=item['SetMode0']['target_mem']
        min_fan_rpm=item['SetMode0']['min_fan_rpm']
        critical_temp=item['SetMode0']['critical_temp']
        SetRpm=item['SetMode2']['SetRpm']
        softVersion=item['softVersion']
        hotGPU=item['hotGPU']
        hotMem=item['hotMem']
        historyBoardFan=item['historyBoardFan'].split(',')[-1]
        rig_online_status=rig_online_status_mess[str(item['rig_online_status'])]
        await message.answer(f" <b>Имя рига</b> -{rig_name}  <b>id рига</b>-{rigId} \n\n <b>Источник управления</b> - {mod_option_hive} \n <b>Статус кулеров GPU</b> - {AlertFan} \n <b>PCI карты с ошибкой по кулеру</b> - {number_gpu_alert} \n <b>Режим внешних кулеров</b> - {selected_mod} \n\n <b><i>Настройки Авто режима</i></b>:\n <b>Таргет GPU</b> min {terget_temp_min} max {terget_temp_max} \n <b>Таргет MEM</b> - {target_mem} \n <b>Минимальная скорость внешних</b> {min_fan_rpm}% <b>Критическая</b> - {critical_temp} \n\n <b><i>Настройки Статичного режима</i></b>: \n <b>Внешние кулера</b> {SetRpm}% \n\n <b><i>Общие данные</i></b>:\n <b>Версия ПО</b> - {softVersion} \n <b>Горячая GPU</b> - {hotGPU} \n <b>Горячая MEM</b> - {hotMem} \n <b>Скорость внешних кулеров</b> - {historyBoardFan} \n <b>Online status</b> - {rig_online_status} \n ",
                             parse_mode=ParseMode.HTML)
    