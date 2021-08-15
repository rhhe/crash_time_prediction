import numpy
import pandas

from utils.TimeTools import TimeTools


class Sample:
    def __init__(self, nc_ip: str, sample_time_hour: float, nc_down_label: bool, nc_down_time_hour=None):
        """
        初始化
        :param nc_ip: 机器IP
        :param sample_time_hour: 采样时间（小时为单位）
        :param nc_down_label: 采样的结果
        :param nc_down_time_hour: 宕机时间（小时为单位）
        """
        self.nc_ip = nc_ip
        self.sample_time_hour = sample_time_hour
        self.nc_down_label = nc_down_label
        self.nc_down_time_hour = nc_down_time_hour

    @staticmethod
    def read_sample_label_csv_file(file_path: str):
        pd_data = pandas.read_csv(file_path)
        sample_data_list: [Sample] = []
        print("Info: label file shape", pd_data.shape)
        n_row = pd_data.shape[0]
        # nc_ip_last = ""
        for i_row in range(n_row):
            if i_row % 50000 == 0:
                print("Info: Label {}/{} is read.".format(i_row, n_row))
            nc_ip = pd_data.iloc[i_row]["nc_ip"]
            # if nc_ip == nc_ip_last:
            #     continue
            # nc_ip_last = nc_ip
            sample_time_hour = TimeTools.time_str_to_hour(pd_data.iloc[i_row]["sample_time"])
            nc_down_label = pd_data.iloc[i_row]["nc_down_label"]
            if numpy.isnan(nc_down_label):
                nc_down_label = False
            sample_data_list.append(Sample(nc_ip, sample_time_hour, nc_down_label))
        return sample_data_list
