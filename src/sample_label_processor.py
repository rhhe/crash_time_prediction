import copy

import pandas

from const import Const
from time_tools import TimeTools


class SampleLabel:
    _bins: [float] = [0.0]
    _n_bins: int = 1
    _exception_type_set: set = {}
    _exception_type_list: list = []

    @classmethod
    def initialize_exception_time_histogram(cls, bins: list):
        cls._bins = bins
        cls._n_bins = len(cls._bins)

    @classmethod
    def get_n_bins(cls):
        return cls._n_bins

    @classmethod
    def get_exception_type_list(cls, recalculate: bool = False):
        if recalculate is False and len(cls._exception_type_list) != 0:
            return cls._exception_type_list
        cls._exception_type_list = list(cls._exception_type_set)
        cls._exception_type_list.sort()
        return cls._exception_type_list

    def __init__(self, nc_ip: str, sample_time_hour: float, nc_down_label: bool, nc_down_time_hour=None):
        self.nc_ip = nc_ip
        self.sample_time_hour = sample_time_hour
        self.nc_down_label = nc_down_label
        self.nc_down_time_hour = nc_down_time_hour
        self.exception_type_to_histogram_mapper: dict = {}

    def refresh_down_time(self, nc_down_time_hour: float or None):
        if nc_down_time_hour is None:
            self.nc_down_time_hour = self.sample_time_hour + Const.N_HOUR_PER_MONTH
            return
        self.nc_down_time_hour = nc_down_time_hour

    def fill_exception(self, exception_type_name: str, exception_time_hour: float):
        if exception_type_name not in self.exception_type_to_histogram_mapper.keys():
            self.exception_type_to_histogram_mapper[exception_type_name] = [0.0] * self._n_bins
        i_bin_fill_in = self._calculate_i_bin(self.sample_time_hour - exception_time_hour)
        if i_bin_fill_in < 0:
            return
        self.exception_type_to_histogram_mapper.get(exception_type_name)[i_bin_fill_in] += 1

    def add_exception_types_to_type_set(self):
        for exception_type in self.exception_type_to_histogram_mapper.keys():
            SampleLabel._exception_type_set.add(exception_type)

    @classmethod
    def _calculate_i_bin(cls, value_fill_in: float) -> int:
        if value_fill_in < cls._bins[0]:
            return -1
        if value_fill_in >= cls._bins[-1]:
            return len(cls._bins) - 1
        i_begin = 0
        i_end = len(cls._bins) - 1
        while True:
            i_middle = (i_begin + i_end) // 2
            if i_middle == i_begin:
                break
            if value_fill_in < cls._bins[i_middle]:
                i_end = i_middle
                continue
            else:
                i_begin = i_middle
                continue
        return i_middle


class SampleLabelListProcessor:
    def __init__(self, file_path: str = None):
        self.sample_label_list: [SampleLabel] = []
        if file_path is not None:
            self.read_sample_label_csv_file(file_path)

    def read_sample_label_csv_file(self, file_path: str):
        pd_data = pandas.read_csv(file_path)
        for row in pd_data:
            nc_ip = row["nc_ip"]
            sample_time_hour = TimeTools.time_str_to_hour(row["sample_time"])
            nc_down_label = row["nc_down_label"]
            self.sample_label_list.append(SampleLabel(nc_ip, sample_time_hour, nc_down_label))


def _test_two_branch_tree():
    n_bin = 10
    bins = [0.4, 0.5, 0.6, 0.9, 1.2,
            1.5, 1.9, 2.3, 5.8, 10.2]
    values = [0.2, 0.45, 0.55, 0.69, 1.0,
              1.23, 1.58, 2.0, 4.4, 10.0, 11.22]
    SampleLabel.initialize_exception_time_histogram(bins=bins)
    for v in values:
        print(v, SampleLabel._calculate_i_bin(v))


if __name__ == '__main__':
    _test_two_branch_tree()
