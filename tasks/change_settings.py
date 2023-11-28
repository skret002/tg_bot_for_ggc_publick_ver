from celery import app
import asyncio
from datetime import time, datetime,timedelta,timezone
from core.utils.make_request import async_chenge_settings,bot_mess_sender
from core.models.model_func import get_double_mod,night_mode_flag,day_mode_flag,get_user_id_tg
from tasks.logging_conf import logg
night_mess='Этот риг переводится на ночные настройки'
day_mess='Этот риг переводится на дневные настройки'
@logg
def select_settings_for_mod(rig_id: int, all_data: dict, mode: str) -> dict:
    obj = list(filter(lambda x: x.rig_id == rig_id, all_data[mode]))[0]
    return {
        "key": obj.rig_key,
        "terget_temp_min": obj.terget_temp_min,
        "terget_temp_max": obj.terget_temp_max,
        "min_fan_rpm": obj.min_fan_rpm,
        "target_mem": obj.target_mem,
        "critical_temp": obj.critical_temp,
        "boost": obj.boost,
        "selected_mod": obj.selected_mod,
        "select_fan": obj.select_fan,
        "static_set_rpm": obj.static_set_rpm,
    }
    # возвращаем из всех полученных объектов, тот который сейчас будем отправлять

@logg
async def change_settings_req(*args):
    await async_chenge_settings(args)

@logg
def get_current_time(hour: int, minute: int) -> datetime:
    delta = timedelta(hours=hour, minutes=minute)
    return datetime.now(timezone.utc) + delta

@logg
def check_time_event(*args) -> dict:
    last_t_start,last_t_end,time_start,time_end,utc,user_id,rig_id,active_night = list(args[0])
    time_now = get_current_time(int(utc.replace(" ", "")[:2]), int(utc.split(" ")[2]))
    print(time_now.replace(tzinfo=None),last_t_end.replace(tzinfo=None), active_night is True)
    if time_now.replace(tzinfo=None) >= last_t_start.replace(tzinfo=None) and active_night is False:
        execute=True
    elif time_now.replace(tzinfo=None)>=last_t_end.replace(tzinfo=None) and active_night is True:
        execute=False
    else:
        execute=None
    if execute != None:
        return {"execute": execute, "rig_id": rig_id,'time_start':time_start,
            'time_end':time_end,'rig_id':rig_id,'user_id':user_id}

async def main():
    all_data = get_double_mod()
    data_switching_mod = list( # распаковываем данные ночного режима для проверки
        map(
            lambda night_mod: [
                night_mod.last_t_start,
                night_mod.last_t_end,
                night_mod.time_start,
                night_mod.time_end, 
                night_mod.user.utc,
                night_mod.user.id,
                night_mod.rig_id,
                night_mod.active,
            ],
            all_data["night_mod"],
        )
    )

    bank_switching_mod=list(map(check_time_event,data_switching_mod)) # проверяем у каких ригов и какой должен быть режим
    tasks_switch_night =list(filter(lambda x: x!=None and x['execute']==True,bank_switching_mod)) #находим кого переключить на ночной режим
    tasks_switch_day =list(filter(lambda x: x!=None and x['execute']==False,bank_switching_mod)) #находим кого переключить на дневной режим
    """готовим запросы на сервер"""
    tasks=[]
    for night in tasks_switch_night:
        settings_night=select_settings_for_mod(night['rig_id'],all_data,'night_mod') #готовим настройки для рига с переходом в ночной
        night_mode_flag(True,night['user_id'],night['time_start'],night['time_end'],night['rig_id'])  # переводим mod в active и считаем время след.
        tasks.append(asyncio.create_task(change_settings_req(settings_night))) # -> отдаем задачу в aiohttp
        bot_mess_sender(get_user_id_tg(night['user_id']), f'{night["rig_id"]} - {night_mess}') #сообщаем юзеру
    for day in tasks_switch_day:    
        settings_day=select_settings_for_mod(day['rig_id'],all_data,'day_mod')#готовим настройки для рига с переходом на дневной
        night_mode_flag(False,day['user_id'],day['time_start'],day['time_end'],day['rig_id']) #переводим mod ночной в inactive и считаем время след
        tasks.append(asyncio.create_task(change_settings_req(settings_day)))
        bot_mess_sender(get_user_id_tg(day['user_id']), f'Риг {day["rig_id"]} - {day_mess}') #сообщаем юзеру
    await asyncio.gather(*tasks) # -> отдаем задачу в aiohttp
    tasks=[]
@logg
@app.shared_task(name='change_settings')
def change_settings():
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main())
