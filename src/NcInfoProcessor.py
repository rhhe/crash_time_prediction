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

    _feature_names: [str] = [
        "physical_model", "cpu_generation_full", "manufacturer",
        "cluster_alias", "cluster_usage", "mem_pn",
        "mem_manufacturer", "bios_version", "os_release",
        "bmc_version"]

    @staticmethod
    def get_feature_names() -> [str]:
        return NcInfo._feature_names

    def get_features(self) -> [str]:
        return [self.physical_model, self.cpu_generation_full, self.manufacturer,
                self.cluster_alias, self.cluster_usage, self.mem_pn,
                self.mem_manufacturer, self.bios_version, self.os_release,
                self.bmc_version]


class NcInfoProcessor:
    def __init__(self, file_path: str = None):
        self.ip_to_info_mapper: {str: NcInfo} = {}
        self.ip_to_features_mapper: {str: [str]} = {}
        if file_path is not None:
            self.read_csv(file_path)

    def read_csv(self, file_path: str):
        data_frame = pandas.read_csv(file_path)
        info_list = data_frame.to_dict("records")
        self.ip_to_info_mapper = {o["nc_ip"]: NcInfo(o) for o in info_list}
        self.ip_to_features_mapper = {o["nc_ip"]: NcInfo(o).get_features() for o in info_list}


def _test():
    nc_info_processor = NcInfoProcessor("../data/train/nc_info.csv")
    for o in nc_info_processor.ip_to_info_mapper.items():
        print(o[0], o[1].__dict__)


if __name__ == '__main__':
    _test()
