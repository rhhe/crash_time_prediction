import logging

import pandas

from TimeTools import TimeTools


class ExceptionProcessor:
    def __init__(self, file_path: str = None):
        self._fp = None
        self._df = None
        self._nc_ip: str = ""
        self._exception_name: str = ""
        self._exception_time_hour: float = -1.0
        self._exception_time_str: str = ""
        self._i_row = 0
        self._n_row = 0
        if file_path is not None:
            self.read_file(file_path)

    def __del__(self):
        if self._fp is None:
            return
        self._fp.close()

    def read_file(self, file_path):
        self._fp = open(file_path, mode='r', encoding='utf-8')
        reader = pandas.read_csv(self._fp, sep=',', iterator=True)
        loop = True
        chunk_size = 100000
        chunks = []
        while loop:
            try:
                chunk = reader.get_chunk(chunk_size)
                chunks.append(chunk)
            except StopIteration:
                loop = False
                print("StopIteration")
        self._df = pandas.concat(chunks, ignore_index=True)
        self._n_row = self._df.shape[0]
        print("Info: exception rows: {}.".format(self._n_row))

    def read_line(self) -> bool:
        if self._i_row >= self._n_row:
            return False
        self._nc_ip = self._df.iloc[self._i_row]["nc_ip"]
        self._exception_name = self._df.iloc[self._i_row]["exception_name"]
        self._exception_time_str = self._df.iloc[self._i_row]["exception_time"]
        self._exception_time_hour = TimeTools.time_str_to_hour(self._exception_time_str)
        return True

    def read(self, i_line: int) -> bool:
        if i_line >= self._n_row:
            return False
        self._nc_ip = self._df.iloc[i_line]["nc_ip"]
        self._exception_name = self._df.iloc[i_line]["exception_name"]
        self._exception_time_str = self._df.iloc[i_line]["exception_time"]
        self._exception_time_hour = TimeTools.time_str_to_hour(self._exception_time_str)
        return True

    def get_nc_ip(self) -> str:
        return self._nc_ip

    def get_exception_type_name(self) -> str:
        return self._exception_name

    def get_exception_time_hour(self) -> float:
        return self._exception_time_hour
