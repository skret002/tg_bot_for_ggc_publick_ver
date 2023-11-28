
import requests

from core.utils.get_data_rigs import get_all_data_rigs
from core.utils.make_request import make_request

single_data={}
def get_all_rigs_status(id_tg: int) ->dict:
    all_rigs_status=[]
    all_data=get_all_data_rigs(id_tg)
    all_license=all_data['data']
    for item in all_license:
        if len(item['attributes']['rig_name']) !=0 and len(item['attributes']['key'])!=0:
            print('item',item['attributes']['key'])
            single_data['the_end_date']=item['attributes']['the_end_date']
            try:
                all_rigs_status.append(make_request(prefix='get_opt_rig_for_bot/',param={"key":item['attributes']['key']},method='GET')['data']['attributes'])
            except (requests.exceptions.JSONDecodeError, TypeError):
                ...
    return all_rigs_status