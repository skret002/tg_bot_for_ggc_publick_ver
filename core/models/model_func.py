from datetime import time, datetime,timedelta,timezone,date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.utils.make_request import make_request, request_all_rig
from core.models.model import (
    UserModel,
    SupportModel,
    NotificationModel,
    DayModeModel,
    NightModeModel,
)

# from model import UserModel,SupportModel,NotificationModel,DayModeModel,NightModeModel
engine = create_engine("sqlite:///user_db.db", echo=True)
Session = sessionmaker(bind=engine)


def search_key_license(all_user_license, external_id_rig):
    for rig in all_user_license["data"]:
        if rig["attributes"]["pk_rig"] == external_id_rig:
            return rig["attributes"]["key"]


def get_filter_id_tg(id_tg: int) -> object:
    # sourcery skip: equality-identity
    with Session() as session:
        return session.query(UserModel).filter_by(id_tg=id_tg).first()


def get_user_id_tg(pk: int) -> object:
    # sourcery skip: equality-identity
    with Session() as session:
        return session.query(UserModel).filter_by(id=pk).first().id_tg


def add_user(name, utc, mail, id_tg, id_server, hash_user, valid=False):
    with Session() as session:
        data = UserModel(
            name=name,
            utc=utc,
            mail=mail,
            id_tg=id_tg,
            id_server=id_server,
            hash_user=hash_user,
            valid=valid,
        )
        session.add(data)
        session.commit()


def get_all_query_user() -> object:
    with Session() as session:
        return session.query(UserModel)


def get_all_query_question() -> object:
    with Session() as session:
        return session.query(SupportModel)


def get_notification_id(rig_id: int) -> int:
    with Session() as session:
        try:
            return session.query(NotificationModel).filter_by(rig_id=rig_id).first().id
        except AttributeError:
            return None

def dell_notification_id(rig_id: int):
    with Session() as session:
        session.query(NotificationModel).filter_by(rig_id=rig_id).delete(
            synchronize_session="fetch"
        )
        session.commit()

def add_notification(**kwargs: dict) -> None:
    kwargs[list(kwargs["dop_args"])[0]] = kwargs["dop_args"][
        list(kwargs["dop_args"])[0]
    ]
    kwargs.pop("dop_args")
    user = get_filter_id_tg(kwargs["id_tg"])
    kwargs.pop("id_tg")
    search_note_id = get_notification_id(kwargs["rig_id"])
    with Session() as session:
        kwargs["user_id"] = user.id
        if search_note_id is not None:
            note_rig = (
                session.query(NotificationModel)
                .filter(NotificationModel.id == search_note_id)
                .update(kwargs, synchronize_session=False)
            )
            session.add_all([user])
        else:
            note_rig = NotificationModel(**kwargs)
            session.add_all([user, note_rig])
        session.commit()

def get_notification():
    with Session() as session:
        return session.query(NotificationModel)

def add_question(user_id, question, id_rig, verified=False):
    with Session() as session:
        data = SupportModel(
            user_id=user_id, question=question, id_rig=id_rig, verified=verified
        )
        session.add(data)
        session.commit()
def response_support(pk: int, status: bool):
    with Session() as session:
        note = session.query(SupportModel).filter_by(id=pk)
        note.update({SupportModel.verified: status}, synchronize_session=False)
        session.commit()
def time_now(pk: int) ->datetime:
    with Session() as session:
        utc = session.query(UserModel).filter_by(id=pk).first().utc
        delta = timedelta(hours=int(utc.replace(" ", "")[:2]), minutes=int(utc.split(" ")[2]))
        return datetime.now(timezone.utc) + delta

def calculate_time_s_e(start_time: str, end_time: str,user_id: int)->datetime:
    s_h=int(start_time.split(':')[0])
    e_h=int(end_time.split(':')[0])
    time_n=time_now(user_id)
    h_start = datetime.strptime(start_time, "%H:%M").strftime("%H") # заданный час старта
    h_now=time_n.strftime("%H") # сейчас час
    if h_now > h_start:
        next_start=datetime.strptime(f'{date.today() + timedelta(days=1)} {start_time}',"%Y-%m-%d %H:%M")# время старта пропущено, переводим на след. сутки
    else:
        next_start=datetime.strptime(f'{date.today()} {start_time}',"%Y-%m-%d %H:%M")
    if e_h < s_h:
        d=next_start.strftime("%d")
        next_end= datetime.strptime(f'{next_start.strftime("%Y-%m-%d")} {end_time}',"%Y-%m-%d %H:%M")+ timedelta(days=1)
    else:
        next_end= datetime.strptime(f'{next_start.strftime("%Y-%m-%d")} {end_time}',"%Y-%m-%d %H:%M")
    return(next_start,next_end)

def add_double_mod(day_mode: dict, nihgt_mode: dict) -> bool:
    s_t = day_mode["time_start"]
    e_t = day_mode["time_end"]
    with Session() as session:
        day_mode = DayModeModel(
            rig_id=str(day_mode["rig_id"]),
            rig_key=str(day_mode["rig_key"]),
            terget_temp_min=str(day_mode["terget_temp_min"]),
            terget_temp_max=str(day_mode["terget_temp_max"]),
            min_fan_rpm=str(day_mode["min_fan_rpm"]),
            target_mem=str(day_mode["target_mem"]),
            critical_temp=str(day_mode["critical_temp"]),
            boost=str(day_mode["boost"]),
            selected_mod=str(day_mode["selected_mod"]),
            select_fan=str(day_mode["select_fan"]),
            static_set_rpm=str(day_mode["static_set_rpm"]),
            updated_on= time_now(day_mode["user_id"]),
            user_id=int(day_mode["user_id"]),
        )
        night_mode = NightModeModel(
            rig_id=str(nihgt_mode["rig_id"]),
            rig_key=str(nihgt_mode["rig_key"]),
            terget_temp_min=str(nihgt_mode["terget_temp_min"]),
            terget_temp_max=str(nihgt_mode["terget_temp_max"]),
            min_fan_rpm=str(nihgt_mode["min_fan_rpm"]),
            target_mem=str(nihgt_mode["target_mem"]),
            critical_temp=str(nihgt_mode["critical_temp"]),
            boost=str(nihgt_mode["boost"]),
            selected_mod=str(nihgt_mode["selected_mod"]),
            select_fan=str(nihgt_mode["select_fan"]),
            static_set_rpm=str(nihgt_mode["static_set_rpm"]),
            time_start=s_t,
            time_end=e_t,
            updated_on = time_now(nihgt_mode["user_id"]),
            last_t_start= calculate_time_s_e(s_t,e_t,nihgt_mode["user_id"])[0],
            last_t_end = calculate_time_s_e(s_t,e_t,nihgt_mode["user_id"])[1],
            user_id=int(nihgt_mode["user_id"]),
        )

        session.add_all([day_mode, night_mode])
        session.commit()

def night_mode_flag(status: bool,user_id:int, time_start: str,time_end: str, rig_id: int) -> None:
    timing=calculate_time_s_e(time_start,time_end,user_id)
    with Session() as session:
        rig = session.query(NightModeModel).filter_by(rig_id=rig_id)
        rig.update({NightModeModel.active: status, NightModeModel.last_t_start:timing[0],
                    NightModeModel.last_t_end:timing[1]}, synchronize_session=False)
        session.commit()
def day_mode_flag(status: bool, rig_id: int) -> None:
    with Session() as session:
        rig = session.query(DayModeModel).filter_by(rig_id=rig_id)
        rig.update({DayModeModel.active: status}, synchronize_session=False)
        session.commit()
def get_double_mod() -> dict:
    with Session() as session:
        all_day_mod = session.query(DayModeModel)
        all_nig_mod = session.query(NightModeModel)
        return {"day_mod": all_day_mod, "night_mod": all_nig_mod}

def dell_double_mod(rig_id: str):
    with Session() as session:
        session.query(DayModeModel).filter_by(rig_id=rig_id).delete(
            synchronize_session="fetch"
        )
        session.query(NightModeModel).filter_by(rig_id=rig_id).delete(
            synchronize_session="fetch"
        )
        session.commit()

def prepare_write_dual_mode(**kwargs):
    dell_double_mod(
        kwargs["rig_id"]
    )  # если такой же конфиг есть для рига удаляем, не перезаписываем
    all_license = request_all_rig(
        prefix="license_all_bot/",
        param={"pk": get_filter_id_tg(kwargs["id_tg"]).id_server},
    )
    license = search_key_license(all_license, kwargs["rig_id"])
    realtime_settings = make_request(
        prefix="get_opt_rig_for_bot/", param={"key": license}, method="GET"
    )["data"]["attributes"]
    day_mode = {
        "rig_id": realtime_settings["rigId"],
        "rig_key": license,
        "terget_temp_min": realtime_settings["SetMode0"]["terget_temp_min"],
        "terget_temp_max": realtime_settings["SetMode0"]["terget_temp_max"],
        "min_fan_rpm": realtime_settings["SetMode0"]["min_fan_rpm"],
        "target_mem": realtime_settings["SetMode0"]["target_mem"],
        "critical_temp": realtime_settings["SetMode0"]["critical_temp"],
        "boost": 0,
        "selected_mod": realtime_settings["SetModeFan"]["selected_mod"],
        "select_fan": realtime_settings["SetModeFan"]["select_fan"],
        "static_set_rpm": realtime_settings["SetMode2"]["SetRpm"],
        "user_id": get_filter_id_tg(kwargs["id_tg"]).id,
        "time_start": kwargs["time_start"],
        "time_end": kwargs["time_end"],
    }
    nihgt_mode = day_mode.copy()
    for item in list(
        kwargs
    ):  # поля которые есть для ночного режима меняем остальное оставляем как в дневном
        nihgt_mode[item] = kwargs[item]
    add_double_mod(day_mode, nihgt_mode)
