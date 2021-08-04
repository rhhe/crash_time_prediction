from datetime import datetime
from Const import Const


class TimeTools:
    def __init__(self):
        pass

    @staticmethod
    def time_str_to_hour(time_str: str) -> float:
        return datetime.strptime(time_str.split('.')[0], Const.TIME_FORMAT).timestamp() / Const.N_MILLISECOND_PER_HOUR
