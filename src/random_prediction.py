import random


def _random_prediction(input_file_name: str, output_file_name: str):
    print(input_file_name)
    with open(input_file_name, mode='r', encoding='utf-8') as fp:
        lines = fp.readlines()[1:]
    index_list_used = [_ for _ in range(len(lines))]
    random.shuffle(index_list_used)
    index_list_used = index_list_used[0: len(lines) // 10]
    index_list_used.sort()
    lines = [lines[i].replace("\n", "")[:-1]+"\n" for i in index_list_used]
    print(output_file_name)
    with open(output_file_name, mode='w', encoding='utf-8') as fp_out:
        fp_out.writelines(lines)


if __name__ == '__main__':
    _random_prediction("../data/test/nc_sample_label.csv", "../data/test/res.csv")
