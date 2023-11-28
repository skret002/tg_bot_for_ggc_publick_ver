from core.utils.get_data_rigs import get_license_rig
from core.utils.make_request import make_request
correspondence = {'gpu':'settings_gpu','mem':'target_mem','critical':'critical_temp','min_fan':'min_fan_rpm','selected_mod':'selected_mod','SetRpm':'SetRpm'}
correspondence_message={'gpu':'Ok, скажу ригу удерживать GPU на ',
                        'mem':'Ok, скажу ригу удерживать MEM на ',
                        'critical': "Ok зададим ригу особые параметры при достижении ",
                        'selected_mod': 'Ok, меняю режим ',
                        'min_fan':'Ok, запрещаю кулерам крутится ниже ',
                        'SetRpm':'Статичный режим установлен'
}

def fill_standart_option(opt: dict,license: str) -> dict:
    return {'terget_temp_min':opt['SetMode0']['terget_temp_min'], 'terget_temp_max': opt['SetMode0']['terget_temp_max'],
            'min_fan_rpm':opt['SetMode0']['min_fan_rpm'],'critical_temp':opt['SetMode0']['critical_temp'],
            'target_mem' : opt['SetMode0']['target_mem'],'boost':opt['SetMode0']['boost'],
            'selected_mod':0,'select_fan':opt['SetModeFan']['select_fan'],'SetRpm':opt['SetMode2']['SetRpm'],
            'key_license':license
            }
        
def prepare_settings(external_id_rig :int, tg_user_id: int, new_option: dict):
    corect_option = {}
    key_for_select_rig=get_license_rig(tg_user_id,external_id_rig)
    realtime_settings=make_request(prefix='get_opt_rig_for_bot/',param={"key":key_for_select_rig},method='GET')['data']['attributes']
    if list(new_option)[0]=='settings_gpu':
        corect_option['terget_temp_min']= int(new_option[list(new_option)[0]])-5
        corect_option['terget_temp_max']= int(new_option[list(new_option)[0]])+5
    else:
        corect_option[list(new_option)[0]]=new_option[list(new_option)[0]]
    standart_opt=fill_standart_option(realtime_settings,key_for_select_rig)
    for name_opt in list(corect_option):
        standart_opt[name_opt]=corect_option[name_opt]
    return standart_opt