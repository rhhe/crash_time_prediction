class Param:
    train_label: str = "./data/train/nc_sample_label.csv"
    train_exception: str = "./data/train/nc_exceptions.csv"
    train_info: str = "./data/train/nc_info.csv"
    feature_train_file: str = "./data/feature_train.csv"

    # test_label: str = "./data/test/nc_sample_label.csv"
    # test_exception: str = "./data/test/nc_exceptions.csv"
    # test_info: str = "./data/test/nc_info.csv"
    # feature_test_file: str = "./data/feature_test.csv"

    test_label: str = "./data/test/round1_B_test_nc_sample_label.csv"
    test_exception: str = "./data/test/round1_B_test_nc_exceptions.csv"
    test_info: str = "./data/test/round1_B_test_nc_info.csv"
    feature_test_file: str = "./data/feature_test_B.csv"
    res_file: str = "./data/res_b.csv"

    train_down: str = "./data/train/nc_down.csv"
    histogram_bins: [float] = [0.0, 1.0, 2.0, 4.0, 8.0, 24.0, 48.0]
    nc_info_embedding_file: str = "./data/nc_info_embedding.json"
    exception_type_file: str = "./data/exception_type.json"

    xgb_param: dict = {
        'booster': 'gbtree',
        # 'slient': 1,

        'objective': 'reg:logistic',
        'eval_metric': 'auc',
        'seed': 1000,

        'eta': 0.2,
        'gamma': 0.1,
        'lambda': 3,
        'max_depth': 8,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 3,
    }
    xgb_n_round: int = 10
