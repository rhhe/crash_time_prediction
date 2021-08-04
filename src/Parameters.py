_param_dict = {
    "train_label": "../data/train/nc_sample_label.csv",
    "train_exception": "../data/train/nc_exceptions.csv",
    "train_info": "../data/train/nc_info.csv",
    "train_down": "../data/train/nc_down.csv",
    "histogram_bins": [0.0, 1.0, 2.0, 4.0, 8.0, 24.0, 48.0],
    "feature_file": "../data/feature.csv",
}


class Parameters:
    def __init__(self, param_dict=None):
        if param_dict is None:
            param_dict = _param_dict
        self.train_label: str = param_dict.get("train_label")
        self.train_exception: str = param_dict.get("train_exception")
        self.train_info: str = param_dict.get("train_info")
        self.train_down: str = param_dict.get("train_down")
        self.histogram_bins: [float] = param_dict.get("histogram_bins")
        self.feature_file: str = param_dict.get("feature_file")
