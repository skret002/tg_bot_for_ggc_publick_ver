from celery import app
from core.models.model_func import get_notification,get_all_query_user,get_user_id_tg
from core.utils.get_data_rigs import get_license_rig
from core.utils.make_request import make_request,bot_mess_sender
from core.models.model import NotificRecTime
import concurrent.futures
from tasks.logging_conf import logg
table_correspondence={'if_off':'rig_online_status' ,'if_hot_gpu':'hotGPU' ,'if_hot_mem':'hotMem' ,
                      'if_fan_rpm':'historyBoardFan' , 'if_fan_rpm_zero':'historyBoardFan'}
table_mess={'if_off':'Риг теперь не доступен' ,'if_hot_gpu':'Наблюдается перегрев по GPU' ,'if_hot_mem':'Наблюдается перегрев по MEM' ,
                      'if_fan_rpm':'Привышена скорость внешних кулеро' , 'if_fan_rpm_zero':'Внешнии кулера не активны!'}
@logg
def prepare_check() ->list:
    data=[]
    all_notis_tasks=get_notification()
    data.extend(
        {
            str(item.rig_id): {
                'user_id':item.user_id,
                'if_off': item.if_off,
                'if_hot_gpu': item.if_hot_gpu,
                'if_hot_mem': item.if_hot_mem,
                'if_fire': item.if_fire,
                'if_fan_rpm': item.if_fan_rpm,
                'if_fan_rpm_zero': item.if_fan_rpm_zero,
            }
        }
        for item in all_notis_tasks
    )
    return data
@logg
def get_actual_rig_data(user_id: int, external_id_rig: str) -> dict:
    tg_user_id = get_all_query_user().filter_by(id = user_id).first().id_tg
    key_for_select_rig=get_license_rig(tg_user_id,external_id_rig)
    state_rig=make_request(prefix='get_opt_rig_for_bot/',param={"key":key_for_select_rig},method='GET')['data']['attributes']
    return {  'external_id_rig':external_id_rig,
            'hotGPU':state_rig['hotGPU'],
           'hotMem':state_rig['hotMem'],
           'historyBoardFan':state_rig['historyBoardFan'].split(',')[-1],
           'rig_online_status':state_rig['rig_online_status'],
        }
@logg
def check_state_rigs(is_notis: dict) -> None:
    id_rig = str(list(is_notis)[0])
    user_id = is_notis[id_rig]['user_id']
    real_time_state = get_actual_rig_data(user_id, id_rig) # данные с ригов в данный момент
    for param in is_notis[id_rig]:
        if param in ['if_fire', 'user_id']:
            continue
        print('>>>!', param,int(is_notis[id_rig][str(param)]), real_time_state[table_correspondence[str(param)]])
        # sourcery skip: merge-nested-ifs
        if (
            int(is_notis[id_rig][str(param)]) != 0
            and int(is_notis[id_rig][str(param)])
            < int(real_time_state[table_correspondence[str(param)]])
            or int(is_notis[id_rig]['if_off'])
            > int(real_time_state[table_correspondence['if_off']])
        ):
            if NotificRecTime().check_time(id_rig) is True:
                NotificRecTime().add_data(id_rig,param)
                bot_mess_sender(get_user_id_tg(user_id), f'Риг {id_rig} - {table_mess[param]}')
@logg
@app.shared_task(name='notis')
def main() ->None:
    check=prepare_check()
    print(check)
    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        executor.map(check_state_rigs, check)

if __name__ == "__main__":
    main()