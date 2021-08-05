import json

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

    cluster_alias_to_i_mapper: {str: int} = {}

    @staticmethod
    def get_feature_names() -> [str]:
        return NcInfo._feature_names

    def get_features(self) -> [str]:
        features = [self.physical_model, self.cpu_generation_full,
                    self.manufacturer, str(NcInfo.cluster_alias_to_i_mapper.get(self.cluster_alias)),
                    self.cluster_usage, self.mem_pn, self.mem_manufacturer,
                    self.bios_version, self.os_release, self.bmc_version]
        features = [str(f) for f in features]
        features = [f.split("_")[-1] for f in features]
        return features

    @staticmethod
    def write_alias_mapper(file_name: str):
        with open(file_name, mode='w', encoding='utf-8') as fp:
            json.dump(NcInfo.cluster_alias_to_i_mapper, fp, ensure_ascii=False)

    @staticmethod
    def read_alias_mapper(file_name: str):
        with open(file_name, mode='r', encoding='utf-8') as fp:
            NcInfo.cluster_alias_to_i_mapper = json.load(fp)


class NcInfoProcessor:
    def __init__(self, file_path: str, embedding_file_name: str, embedding_used: bool):
        self.ip_to_info_mapper: {str: NcInfo} = {}
        self.ip_to_features_mapper: {str: [str]} = {}
        self.cluster_alias_to_i_mapper: {str: int} = {}
        if file_path is not None:
            self.read_csv(file_path)
            if embedding_used is True:
                self.embedding_cluster_alias()
                NcInfo.write_alias_mapper(embedding_file_name)
            else:
                NcInfo.read_alias_mapper(embedding_file_name)
            self.make_features()

    def read_csv(self, file_path: str):
        data_frame = pandas.read_csv(file_path)
        info_list = data_frame.to_dict("records")
        self.ip_to_info_mapper = {o["nc_ip"]: NcInfo(o) for o in info_list}

    def embedding_cluster_alias(self):
        cluster_alias_list: list = [str(nc_info.cluster_alias) for nc_info in self.ip_to_info_mapper.values()]
        cluster_alias_list.sort()
        NcInfo.cluster_alias_to_i_mapper = {cluster_alias_list[i]: i for i in range(len(cluster_alias_list))}

    def make_features(self):
        self.ip_to_features_mapper = {k: self.ip_to_info_mapper.get(k).get_features()
                                      for k in self.ip_to_info_mapper.keys()}

    def get_features(self, nc_ip: str):
        res = self.ip_to_features_mapper.get(nc_ip)
        return [0 for _ in range(10)] if res is None else res


def _test():
    nc_info_processor = NcInfoProcessor("../data/train/nc_info.csv")
    for o in nc_info_processor.ip_to_info_mapper.items():
        print(o[0], o[1].__dict__)


if __name__ == '__main__':
    _test()
