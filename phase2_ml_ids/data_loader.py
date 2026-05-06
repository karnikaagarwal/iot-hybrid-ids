import pandas as pd

def load_data():
    base = "/home/ubuntu-iot-hub/iotsec-datasets/public/UNSW/"

    train = pd.read_csv(base + "UNSW_NB15_training-set.csv")
    test = pd.read_csv(base + "UNSW_NB15_testing-set.csv")

    return train, test
