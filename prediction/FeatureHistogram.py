import json
from utils.Const import Const
from data_process.Sample import Sample


class FeatureHistogram(Sample):
    """
    特征工程，是用于原有的机器的属性的标签之外，利用各种日志信息的统计结果生成的各个时间段的直方图信息.
    其中可以调节的关键参数，就是直方图的统计的bin的设置。
    """
    # 直方图统计的分桶信息，当有n个值的时候，表示的是，n个边界值，分成n个桶，最后一个桶的上界是正无穷。
    _bins: [float] = [0.0]
    # 桶的个数
    _n_bins: int = 1
    # 异常信息类型集合
    _exception_type_set: set = set()
    # 异常信息类型列表
    _exception_type_list: list = []

    @classmethod
    def initialize_exception_time_histogram(cls, bins: list) -> None:
        """
        初始化直方图的边界值，因为这些边界值，并不是特征信息，而是参数。
        :param bins: 分桶的下界列表
        :return:
        """
        cls._bins = bins
        cls._n_bins = len(cls._bins)

    @classmethod
    def get_n_bins(cls) -> int:
        """
        获取桶的个数
        :return: 桶的个数
        """
        return cls._n_bins

    @classmethod
    def get_exception_type_list(cls, recalculate: bool = False) -> [str]:
        """
        获取异常类型列表
        :param recalculate: 是否重新计算，默认不重新计算
        :return: 返回异常类型列表
        """
        if recalculate is False and len(cls._exception_type_list) != 0:
            return cls._exception_type_list
        cls._exception_type_list = list(cls._exception_type_set)
        cls._exception_type_list.sort()
        return cls._exception_type_list

    def __init__(self, sample: Sample, down_info_mapper: dict = None):
        """
        :param sample: 抽样类实例
        """
        super().__init__(sample.nc_ip, sample.sample_time_hour,
                         sample.nc_down_label, sample.nc_down_time_hour)
        if down_info_mapper is not None:
            self.nc_down_time_hour = down_info_mapper.get(self.nc_ip)
        self._refresh_down_time()
        self._exception_type_to_histogram_mapper: dict = {}

    def _refresh_down_time(self):
        """
        刷新宕机时间，如果没有宕机，将宕机时间刷新为一个月之后。
        :return:
        """
        if self.nc_down_time_hour is None:
            if self.nc_down_label:
                self.nc_down_time_hour = self.sample_time_hour + 24.0
            else:
                self.nc_down_time_hour = self.sample_time_hour + Const.N_HOUR_PER_MONTH

    def fill_exception(self, exception_type_name: str, exception_time_hour: float) -> None:
        """
        把一个日志信息中的异常信息，丢进直方图。
        :param exception_type_name: 异常类型名称
        :param exception_time_hour: 异常日志时间（小时为单位）
        :return:
        """
        if exception_type_name not in self._exception_type_to_histogram_mapper.keys():
            self._exception_type_to_histogram_mapper[exception_type_name] = [0.0] * self._n_bins
        i_bin_fill_in = self._calculate_i_bin(self.sample_time_hour - exception_time_hour)
        if i_bin_fill_in < 0:
            return
        self._exception_type_to_histogram_mapper[exception_type_name][i_bin_fill_in] += 1

    @classmethod
    def _calculate_i_bin(cls, value_fill_in: float) -> int:
        """
        计算bin的编号
        :param value_fill_in: 丢入直方图的值。
        :return: 直方图的bin的index，-1表示异常在采样时间之后发生，不统计。
        """
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

    def add_exception_types_to_type_set(self):
        for exception_type in self._exception_type_to_histogram_mapper.keys():
            FeatureHistogram._exception_type_set.add(exception_type)

    @staticmethod
    def make_exception_type_list(file_name: str = None):
        FeatureHistogram._exception_type_list = [o for o in FeatureHistogram._exception_type_set]
        FeatureHistogram._exception_type_list.sort()
        if file_name is None:
            return
        with open(file_name, mode='w', encoding='utf-8') as fp:
            json.dump(FeatureHistogram._exception_type_list, fp, ensure_ascii=False)

    @staticmethod
    def read_exception_type_list(file_name: str):
        with open(file_name, mode='r', encoding='utf-8') as fp:
            FeatureHistogram._exception_type_list = json.load(fp)

    @staticmethod
    def get_feature_names():
        names: [str] = []
        for exception_type in FeatureHistogram._exception_type_list:
            names += [exception_type + str(i) for i in range(FeatureHistogram._n_bins)]
        return names

    def make_empty_histogram_with_unused_exception_types(self):
        for exception_type in FeatureHistogram._exception_type_list:
            if exception_type in self._exception_type_to_histogram_mapper.keys():
                continue
            self._exception_type_to_histogram_mapper[exception_type] = [0.0 for _ in range(self.get_n_bins())]

    def get_features(self):
        features: [int] = []
        for exception_type in FeatureHistogram._exception_type_list:
            features += self._exception_type_to_histogram_mapper.get(exception_type)
        return features

    def get_delta_time_hour(self):
        if self.nc_down_time_hour is None or self.sample_time_hour is None:
            return 720.0
        return self.nc_down_time_hour - self.sample_time_hour
