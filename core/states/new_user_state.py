from aiogram.fsm.state import StatesGroup,State
class StepNewUser(StatesGroup):
    GET_EMAIL=State()
    GET_CODE=State()
class MenuClass(StatesGroup):
    GET_FIRST_MENU=State()
    NOTIFICATION_MENU=State()
    CHANGE_SETTINGS_MENU=State()
    
class NotificationMenuClass(StatesGroup):
    GPU_TEMP=State()
    GPU_MEM=State()
    RPM_FAN=State()
    ON_OFF=State()
    FAN_ZERO=State()
    HASH_LOW=State()
    CAT=State()
class SelectRigsClass(StatesGroup):
    select_rigs=State()
    
class SettingsState(StatesGroup):
    gpu_temp=State()
    mem_temp=State()
    min_fan=State()
    critical=State()
    change_mod=State()
    night_mode=State()
    select_rigs=State()
    get_permission=State()
    static_rpm=State()
    
class NightModeState(StatesGroup):
    rig_id=State()
    rig_key=State()
    terget_cpu=State()
    terget_temp_min=State()
    terget_temp_max=State()
    min_fan_rpm=State()
    target_mem=State()
    critical_temp=State()
    boost=State()
    selected_mod=State()
    select_fan=State()
    static_set_rpm=State()
    time_start=State()
    time_end=State()
    active=State()
    inactiva=State()
    delete_mod=State()
    
class SupportState(StatesGroup):
    await_mess=State()
    get_id_rig=State()