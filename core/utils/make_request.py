import aiohttp
import requests
from requests.adapters import HTTPAdapter, Retry
from json.decoder import JSONDecodeError
from core.settings import settings
from dotenv import load_dotenv
import os

load_dotenv()
def get_token()->str:
    url = f'{settings.server.url}:{settings.server.port}/api-token-auth/'
    payload = {
    "username": os.getenv('AUF_SERVER_NAME'),
    "password": os.getenv('AUF_SERVER_PASS')
}
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()['token']
def get_session():
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
async def async_chenge_settings(*args,host=settings.server.url,port=settings.server.port):
    settings = args[0][0]
    headers = {"Authorization": f"Token {get_token()}"},
    url=f'{host}:{port}/set_option_rig_from_bot/'
    params={
    'key_license':settings['key'],
    'terget_temp_min':settings['terget_temp_min'],
    'terget_temp_max': settings['terget_temp_max'],
    'min_fan_rpm':settings['min_fan_rpm'],
    'target_mem':settings['target_mem'],
    'critical_temp':settings['critical_temp'],
    'boost':settings['boost'],
    'selected_mod':settings['selected_mod'],
    'select_fan':settings['select_fan'],
    'SetRpm':settings['static_set_rpm']}
    async with aiohttp.ClientSession(headers=headers[0]) as session:
        async with session.post(url,params=params) as response:
            await response.text()
def make_request(url: str=settings.server.url,prefix: str=None, port: str=settings.server.port,  data=None, param=None,method :str='POST'):
    headers = {"Authorization": f"Token {get_token()}"}
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    url = f'{url}:{port}/{prefix}'  #для сервера
    response = session.request(method, url, data=data, headers=headers, params=param)
    print('response',response)
    try:
        return(response.json())
    except JSONDecodeError:
        return response.text

def request_all_rig(url: str=settings.server.url,prefix: str=None, port: str=settings.server.port,  data=None, param=None):
    headers = {"Authorization": f"Token {get_token()}"}
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=30)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    url = f'{url}:{port}/{prefix}'  #для сервера
    response = session.request("GET", url, data=data, headers=headers, params=param)
    try:
        return(response.json())
    except JSONDecodeError:
        return response.text

def bot_mess_sender(chat_id:int, message: str) ->str:
    url = f"https://api.telegram.org/bot{settings.bot.token}/sendMessage"
    querystring = {"chat_id":chat_id,"text":message}
    payload = ""
    headers = {"User-Agent": "ggc.center"}
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return response.text