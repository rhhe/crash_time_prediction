import pandas

from src.TimeTools import TimeTools
from src.Parameters import Parameters
from src.ExceptionProcessor import ExceptionProcessor
from src.NcInfoProcessor import NcInfoProcessor, NcInfo
from src.FeatureHistogram import FeatureHistogram, Sample


def _make_ip_to_sample_index_list_mapper(samples: [Sample]) -> {str: [int]}:
    mapper: {str: [int]} = {}
    for i in range(len(samples)):
        nc_ip = samples[i].nc_ip
        mapper.setdefault(nc_ip, [])
        mapper[nc_ip].append(i)
    return mapper


def make_features():
    param = Parameters()
    print("Info: ExceptionProcessor(): start.")
    exception_processor = ExceptionProcessor(file_path=param.train_exception)
    print("Info: NcInfoProcessor(): start.")
    nc_info_processor = NcInfoProcessor(file_path=param.train_info)
    print("Info: initialize_exception_time_histogram(): start.")
    FeatureHistogram.initialize_exception_time_histogram(bins=param.histogram_bins)
    print("Info: read_sample_label_csv_file(): start.")
    samples: [Sample] = Sample.read_sample_label_csv_file(file_path=param.train_label)
    hist_features: [FeatureHistogram] = [FeatureHistogram(o) for o in samples]
    print("Info: _make_ip_to_sample_index_list_mapper(): start.")
    ip_to_sample_index_list_mapper: {str: [int]} = _make_ip_to_sample_index_list_mapper(samples)
    print("Info: exception_processor.read_line(): start.")
    i_line = 0
    while exception_processor.read_line():
        if i_line % 50000 == 0:
            print("Info: exception_processor.read_line(): i_line: {}.".format(i_line))
        if i_line == 500000:
            break
        i_line += 1
        nc_ip = exception_processor.get_nc_ip()
        i_hist_list = ip_to_sample_index_list_mapper.get(nc_ip)
        if i_hist_list is None:
            continue
        exception_type_name = exception_processor.get_exception_type_name()
        exception_time_hour = exception_processor.get_exception_time_hour()
        for i_hist in i_hist_list:
            hist_features[i_hist].fill_exception(exception_type_name, exception_time_hour)
    for hist_feature in hist_features:
        hist_feature.add_exception_types_to_type_set()
    FeatureHistogram.make_exception_type_list()
    for hist_feature in hist_features:
        hist_feature.make_empty_histogram_with_unused_exception_types()
    print(FeatureHistogram.get_exception_type_list())
    data_list = [
        [h.get_delta_time_hour()] + nc_info_processor.ip_to_features_mapper.get(h.nc_ip) + h.get_features()
        for h in hist_features]
    cols: [str] = ["delta_hour"] + NcInfo.get_feature_names() + FeatureHistogram.get_feature_names()
    df = pandas.DataFrame(columns=cols, data=data_list)
    df.to_csv(param.feature_file, encoding='utf-8')


if __name__ == '__main__':
    make_features()
