import json
import logging

import pandas

from parameter_parser import Param
from exception_processor import ExceptionProcessor


class DataParser:
    def __init__(self, param: Param):
        self._param = param
        self._exception_processor: ExceptionProcessor = ExceptionProcessor()
        self._read_files()

    @staticmethod
    def _read_file(path_name: str):
        logging.info(msg="Read file {}".format(path_name))
        data = pandas.read_csv(path_name, nrows=20)
        print(data.head().to_string())
        return data

    def _read_files(self):
        logging.warning(msg="DataParser base class should be called.")


class TrainDataParser(DataParser):
    def __init__(self, param: Param):
        super().__init__(param)

    def _read_files(self):
        # self._label_data = self._read_file(self._param.train_label)
        self._exception_processor.read_exceptions_info_from_csv_file(self._param.train_exception)
        # self._info_data = self._read_file(self._param.train_info)
        # self._down_data = self._read_file(self._param.train_down)


def _test():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s]%(asctime)s.%(msecs)03d,f=%(filename)s,l=%(lineno)d,%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    with open("./parameters.json", mode='r', encoding='utf-8') as fp:
        param = Param(json.load(fp=fp))
        print(param.__dict__)
    train_data_parser = TrainDataParser(param)


if __name__ == '__main__':
    _test()
