import random

import xgboost as xgb
import numpy as np
import pandas as pd

from src.Param import Param


def train_and_test():
    random.seed(0)

    df_train = pd.read_csv(Param.feature_train_file).fillna(0)
    df_train.replace("None", 0, inplace=True)
    print(df_train.head().to_string())
    matrix_train = np.array(df_train)
    n_row, n_col = np.shape(matrix_train)
    for i_row in range(n_row):
        label = matrix_train[i_row][1]
        # 1 表示时间长，0表示时间短
        matrix_train[i_row][1] = 1 if label > 120. else 0
    train_data = xgb.DMatrix(data=matrix_train[:, 2:], label=matrix_train[:, 1])

    count_break_down = 0
    for i_row in range(n_row):
        count_break_down += matrix_train[i_row][1]
    break_down_ratio = 1. - float(count_break_down) / float(n_row)
    print("Info: break down ratio = {}.".format(break_down_ratio))

    df_test = pd.read_csv(Param.feature_test_file).fillna(0)
    df_test.replace("None", 0, inplace=True)
    print(df_test.head().to_string())
    matrix_test = np.array(df_test)
    test_data = xgb.DMatrix(data=matrix_test[:, 2:])

    model = xgb.train(Param.xgb_param, train_data, Param.xgb_n_round)
    test_label = model.predict(test_data)
    test_label = test_label.T.tolist()
    i_label_list = [i for i in range(len(test_label))]
    i_label_list.sort(key=lambda i_label: test_label[i_label])
    i_label_list_break_down = i_label_list[:int(len(i_label_list) * break_down_ratio)]
    test_label_sorted = [test_label[i_label] for i_label in i_label_list_break_down]
    # print(test_label_sorted)

    with open(Param.test_label, mode='r', encoding='utf-8') as fp:
        lines = fp.readlines()[1:]
    lines = [lines[i] for i in i_label_list_break_down]
    lines = [",".join(o.split(",")[0:2])+"\n" for o in lines]
    with open(Param.res_file, mode='w', encoding='utf-8') as fp_out:
        fp_out.writelines(lines)


if __name__ == '__main__':
    train_and_test()
