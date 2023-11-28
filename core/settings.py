from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()

@dataclass
class Bots:
    token: str
    
@dataclass
class Server:
    url: str
    port: str
    auf_server_name: str
    auf_server_pass: str

@dataclass
class Settings:
    bot:Bots
    server:Server   
def get_settings():
    return Settings(
    bot=Bots(
        token=os.getenv('TOKEN'),
    ),
    server=Server(
        url = os.getenv('URL'),
        port = os.getenv('PORT'),
        auf_server_name = os.getenv('AUF_SERVER_NAME'),
        auf_server_pass = os.getenv('AUF_SERVER_PASS')
    ))
settings=get_settings()