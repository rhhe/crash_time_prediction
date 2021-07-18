import pandas

from time_tools import TimeTools


class DownInfoProcessor:
    def __init__(self, file_path: str = None):
        self.nc_to_down_time_hour_mapper: dict = {}
        if file_path is not None:
            self.read_down_info_csv_file(file_path)

    def read_down_info_csv_file(self, file_path: str):
        pd_data = pandas.read_csv(file_path)
        for row in pd_data:
            nc_ip = row["nc_ip"]
            down_time_hour = TimeTools.time_str_to_hour(row["down_start_time"])
            self.nc_to_down_time_hour_mapper[nc_ip] = down_time_hour

    def get_nc_to_down_time_hour_mapper(self) -> dict:
        return self.nc_to_down_time_hour_mapper

    def get_down_time_hour(self, nc_ip: str) -> float or None:
        return self.nc_to_down_time_hour_mapper.get(nc_ip)
