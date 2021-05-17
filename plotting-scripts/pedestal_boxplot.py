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

        series.append(list(map(lambda x: x[1], out)))
        xAxis.append(re.search(r'\d\d\d\d_\d\d_\d\d',file.strip()).group(0))

    fig = plt.figure()
    plt.xticks([], xAxis)
    bp = plt.boxplot(series)

    plt.show()

if __name__ == '__main__':
    boxplot(sys.argv[1])
