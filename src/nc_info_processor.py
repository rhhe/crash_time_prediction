import pandas


class NcInfo:
    def __init__(self, mapper: dict = None):
        self.nc_ip: str = ""
        self.physical_model: str = ""
        self.cpu_generation_full: str = ""
        self.manufacturer: str = ""
        self.cluster_alias: str = ""
        self.cluster_usage: str = ""
        self.mem_pn: str = ""
        self.mem_manufacturer: str = ""
        self.bios_version: str = ""
        self.os_release: str = ""
        self.bmc_version: str = ""
        if mapper is not None:
            self.__dict__.update(mapper)


class NcInfoProcessor:
    def __init__(self, file_path: str = None):
        self.ip_to_info_mapper: {str: NcInfo} = None
        if file_path is not None:
            self.read_csv(file_path)

    def read_csv(self, file_path: str):
        data_frame = pandas.read_csv(file_path)
        info_list = data_frame.to_dict("records")
        self.ip_to_info_mapper = {o["nc_ip"]: NcInfo(o) for o in info_list}


def _test():
    nc_info_processor = NcInfoProcessor("../data/train/nc_info.csv")
    for o in nc_info_processor.ip_to_info_mapper.items():
        print(o[0], o[1].__dict__)


if __name__ == '__main__':
    _test()