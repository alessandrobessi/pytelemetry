import datetime
from typing import List, Union


def get_lap_time(data: List, return_float: bool = False) -> Union[str, float]:
    time, speed, throttle, steer, brake, clutch, gear, engine, drs = zip(*data)
    if return_float:
        return time[-1]
    return str(datetime.timedelta(seconds=time[-1]))[3:]
