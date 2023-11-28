from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    create_engine,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime,timezone,timedelta
from pathlib import Path
from sqlalchemy import event
import os
engine = create_engine("sqlite:///user_db.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
BASE_DIR = Path(__file__).resolve().parent.parent


class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mail = Column(String)
    id_tg = Column(Integer)
    id_server = Column(Integer)
    utc = Column(Integer)
    valid = Column(Boolean)
    hash_user = Column(Integer)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    support = relationship("SupportModel", back_populates="user")
    notification = relationship("NotificationModel", back_populates="user")
    day_mode = relationship("DayModeModel", back_populates="user")
    night_mode = relationship("NightModeModel", back_populates="user")

    def __repr__(self):
        return f"UserModel({self.id},{self.name},{self.mail},{self.id_tg},{self.id_server},{self.valid},{self.created_on},{self.updated_on})"

    def db_init(self):
        Base.metadata.create_all(engine)


class NotificationModel(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True)
    rig_id = Column(Integer, nullable=False)
    if_off = Column(Boolean, default=False)
    if_hot_gpu = Column(Integer, default=0)
    if_hot_mem = Column(Integer, default=0)
    if_fire = Column(Boolean, default=False)
    if_fan_rpm = Column(Integer, default=0)
    if_fan_rpm_zero = Column(Integer, default=0)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="notification")

    def __new__(cls, *args, **kwargs):  # лучше бы я заюзал Pydantic
        try:
            initializer = cls.__initializer
        except AttributeError:
            cls.__initializer = initializer = cls.__init__
            cls.__init__ = lambda *a, **k: None
        added_args = {
            name: kwargs.pop(name)
            for name in list(kwargs.keys())
            if name not in cls.__annotations__
        }
        ret = object.__new__(cls)
        initializer(ret, **kwargs)
        for new_name, new_val in added_args.items():
            setattr(ret, new_name, new_val)
        return ret

    def __repr__(self):
        return f"NotificationModel({self.id},{self.user},{self.rig_id},{self.if_off},{self.if_hot_gpu},{self.if_hot_mem},{self.if_fire},{self.if_fan_rpm})"


class SupportModel(Base):
    __tablename__ = "support"
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    id_rig = Column(String(60), nullable=False)
    verified = Column(Boolean, default=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="support")

    def __repr__(self):
        return f"<SupportModel user#{self.user_id} question#{self.question}>"


class DayModeModel(Base):
    __tablename__ = "day_mode"
    id = Column(Integer, primary_key=True)
    rig_id = Column(String(50), nullable=False)
    rig_key = Column(String(256), nullable=False)
    terget_temp_min = Column(String(5), nullable=False)
    terget_temp_max = Column(String(5), nullable=False)
    min_fan_rpm = Column(String(5), nullable=False)
    target_mem = Column(String(5), nullable=False)
    critical_temp = Column(String(5), nullable=False)
    boost = Column(String(5), nullable=False)
    selected_mod = Column(String(5), nullable=False)
    select_fan = Column(String(5), nullable=False)
    static_set_rpm = Column(String(5), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    updated_on = Column(DateTime(), default=None)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="day_mode")

    def __repr__(self):
        return f"<DayModeModel rig_id#{self.rig_id} terget_temp_min#{self.terget_temp_min} terget_temp_max#{self.terget_temp_max} min_fan_rpm#{self.min_fan_rpm} target_mem#{self.target_mem} critical_temp#{self.critical_temp} selected_mod#{self.selected_mod}       select_fan#{self.select_fan} static_set_rpm#{self.static_set_rpm} user_id#{self.user_id}>"


class NightModeModel(Base):
    __tablename__ = "night_mode"
    id = Column(Integer, primary_key=True)
    rig_id = Column(String(50), nullable=False)
    rig_key = Column(String(256), nullable=False)
    terget_temp_min = Column(String(5), nullable=False)
    terget_temp_max = Column(String(5), nullable=False)
    min_fan_rpm = Column(String(5), nullable=False)
    target_mem = Column(String(5), nullable=False)
    critical_temp = Column(String(5), nullable=False)
    boost = Column(String(5), nullable=False)
    selected_mod = Column(String(5), nullable=False)
    select_fan = Column(String(5), nullable=False)
    static_set_rpm = Column(String(5), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    time_start = Column(String(5), nullable=True)
    time_end = Column(String(5), nullable=True)
    last_t_start=Column(DateTime(), nullable=True, default=None)
    last_t_end=Column(DateTime(), nullable=True, default=None)
    created_on = Column(DateTime(), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    updated_on = Column(DateTime(), nullable=True, default=None)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("UserModel", back_populates="night_mode")

    def __repr__(self):
        return f"<DayModeModel rig_id#{self.rig_id} terget_temp_min#{self.terget_temp_min} terget_temp_max#{self.terget_temp_max} min_fan_rpm#{self.min_fan_rpm} target_mem#{self.target_mem} critical_temp#{self.critical_temp} selected_mod#{self.selected_mod} select_fan#{self.select_fan} static_set_rpm#{self.static_set_rpm} user_id#{self.user_id}>"


class NotificRecTime(Base):
    __tablename__ = "notific_rec_time"
    id = Column(Integer, primary_key=True)
    rig_id = Column(Integer, nullable=False)
    param = Column(String(50), nullable=False)
    last_time = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def check_time(self, rig_id: int) -> bool:
        with Session() as session:
            note = session.query(NotificRecTime).filter_by(rig_id=rig_id).first()
            if note is None:
                return True
            return note.last_time + timedelta(minutes=10) < datetime.now()

    def add_data(self, rig_id: int, param: str) -> None:
        with Session() as session:
            note = session.query(NotificRecTime).filter_by(rig_id=rig_id)
            try:
                if note.first().rig_id:
                    note.update(
                        {NotificRecTime.param: param}, synchronize_session=False
                    )
            except AttributeError as e:
                note = NotificRecTime(rig_id=rig_id, param=param)
                session.add(note)
            session.commit()

    def __repr__(self):
        return f"NotificRecTime: id-{self.id}, rig_id={self.frig_id}, param={self.fparam}, last_time-{self.last_time}"
    
if __name__ == "__main__" and os.path.exists(f"{BASE_DIR}/user_db.db") is False:

    Base.metadata.create_all(engine)
