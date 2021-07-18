class Param:
    def __init__(self, param_dict: dict):
        self.train_label: str = param_dict.get("train_label")
        self.train_exception: str = param_dict.get("train_exception")
        self.train_info: str = param_dict.get("train_info")
        self.train_down: str = param_dict.get("train_down")
