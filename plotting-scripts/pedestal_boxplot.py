import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import re

def boxplot(fileList):
    f = open(fileList, "r")

    xAxis = []
    series = []
    for file in f:
        f1 = open (file.strip(), "r")
        out = json.loads(f1.read())
        out = list(map(lambda x: (x[0], np.mean(x[2]), np.std(x[2])), out))

        series.append(list(map(lambda x: x[1], out)))
        timestamp = re.search(r'\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d',file.strip()).group(0)
        xAxis.append(f"{timestamp[:4]}/{timestamp[5:7]}/{timestamp[8:10]}\n{timestamp[11:13]}:{timestamp[14:16]}:{timestamp[17:19]}")

    fig = plt.figure(figsize=[12.8, 9.6])
    bp = plt.boxplot(series, labels = xAxis)
    plt.savefig('plots/boxplot_Fliers.png', transparent=True)

    fig = plt.figure(figsize=[12.8, 9.6])
    bp = plt.boxplot(series, labels = xAxis, showfliers=False)
    plt.savefig('plots/boxplot_noFliers.png', transparent=True)

if __name__ == '__main__':
    boxplot(sys.argv[1])
