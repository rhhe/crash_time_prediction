from prediction.make_features import make_features
from prediction.train_and_test import train_and_test


def main():
    make_features(is_train=True)
    make_features(is_train=False)
    train_and_test()


if __name__ == '__main__':
    main()
