import csv

def save_sample(features, label):

    with open("dataset.csv","a") as f:
        writer = csv.writer(f)
        writer.writerow(features + [label])
