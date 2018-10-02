import datetime
import os
from typing import List, Union


def get_lap_time(data: List, return_float: bool = False) -> Union[str, float]:
    time, speed, throttle, steer, brake, clutch, gear, engine, drs = zip(*data)
    lap_time = round(time[-1], 3)
    if return_float:
        return lap_time
    return str(datetime.timedelta(seconds=lap_time))[3:11]


def create_sessions_dir() -> None:
    if not os.path.exists(os.path.join(os.getcwd(), 'sessions')):
        os.makedirs(os.path.join(os.getcwd(), 'sessions'))
