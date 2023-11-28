from core.utils.make_request import request_all_rig
from core.models.model_func import get_filter_id_tg,search_key_license
def get_all_name_rigs(tg_id: int) -> dict:
    id_user_serv = get_filter_id_tg(tg_id).id_server
    all_user_license=request_all_rig(prefix='license_all_bot/',param={"pk":id_user_serv})
    return {
        item['attributes']['rig_name']:item['attributes']['pk_rig']
        for item in all_user_license['data']
        if len(item['attributes']['rig_name'])
    }
def get_all_data_rigs(tg_id: int) -> dict:
    id_user_serv = get_filter_id_tg(tg_id).id_server
    return request_all_rig(prefix='license_all_bot/',param={"pk":id_user_serv})

def get_license_rig(tg_id: int, external_id_rig: int):
    id_user_serv = get_filter_id_tg(tg_id).id_server
    all_user_license=request_all_rig(prefix='license_all_bot/',param={"pk":id_user_serv})
    return search_key_license(all_user_license,external_id_rig)

