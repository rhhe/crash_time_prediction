import logging

from time_tools import TimeTools


class ExceptionProcessor:
    def __init__(self, file_path: str = None):
        self._fp = None
        self._nc_ip: str = ""
        self._exception_name: str = ""
        self._exception_time_hour: float = -1.0
        self._exception_time_str: str = ""
        if file_path is not None:
            self.read_file(file_path)

    def __del__(self):
        if self._fp is None:
            return
        self._fp.close()

    def read_file(self, file_path):
        self._fp = open(file_path, mode='r', encoding='utf-8')
        self._fp.readline()

    def read_line(self) -> bool:
        if not self._fp:
            logging.info("read exception file to eof with fp.")
            return False
        info_row = self._fp.readline()
        if len(info_row) == 0:
            logging.info("read exception file to eof with len(row) is 0.")
            return False
        [self._nc_ip, self._exception_name, self._exception_time_str] = info_row.split(",")[0:3]
        self._exception_time_hour = TimeTools.time_str_to_hour(self._exception_time_str)
        return True

    def get_nc_ip(self) -> str:
        return self._nc_ip

    def get_exception_type_name(self) -> str:
        return self._exception_name

    def get_exception_time_hour(self) -> float:
        return self._exception_time_hour
