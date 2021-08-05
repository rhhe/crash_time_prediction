import pandas

from TimeTools import TimeTools


class DownInfoProcessor:
    def __init__(self, file_path: str = None):
        self.nc_to_down_time_hour_mapper: dict = {}
        if file_path is not None:
            self.read_down_info_csv_file(file_path)

    def read_down_info_csv_file(self, file_path: str):
        pd_data = pandas.read_csv(file_path)
        n_row = pd_data.shape[0]
        for i_row in range(n_row):
            nc_ip = pd_data.iloc[i_row]["nc_ip"]
            self.nc_to_down_time_hour_mapper[nc_ip] = TimeTools.time_str_to_hour(pd_data.iloc[i_row]["down_start_time"])

    def get_nc_to_down_time_hour_mapper(self) -> dict:
        return self.nc_to_down_time_hour_mapper

    def get_down_time_hour(self, nc_ip: str) -> float or None:
        return self.nc_to_down_time_hour_mapper.get(nc_ip)
