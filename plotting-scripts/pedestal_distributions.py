import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import re

def distributionPlots(fileList):
    f = open(fileList, "r")

    cumMean = plt.figure(1)
    cumMeanLog = plt.figure(2)
    cumStd = plt.figure(3)
    cumStdLog = plt.figure(4)

    for file in f:
        f1 = open (file.strip(), "r")
        out = json.loads(f1.read())
        out = list(map(lambda x: (x[0], np.mean(x[2]), np.std(x[2])), out))

        runNo = re.search(r'\d\d\d\d_\d\d_\d\d_\d\d_\d\d_\d\d',file.strip()).group(0)

        plt.figure(1)
        plt.hist(list(map(lambda x: x[1], out)), label=runNo, bins=200, histtype='step')

        plt.figure(2)
        plt.hist(list(map(lambda x: x[1], out)), label=runNo, bins=200, histtype='step')

        plt.figure(3)
        plt.hist(list(map(lambda x: x[2], out)), label=runNo, bins=200, histtype='step')

        plt.figure(4)
        plt.hist(list(map(lambda x: x[2], out)), label=runNo, bins=200, histtype='step')


        fig = plt.figure()
        plt.hist(list(map(lambda x: x[1], out)), bins=200, histtype='step')
        plt.xlabel('mean ADC')
        plt.ylabel('channel count')
        plt.savefig(f"plots/{runNo}_mean.png", transparent=True)
        plt.close()

        fig = plt.figure()
        plt.hist(list(map(lambda x: x[2], out)), bins=200, histtype='step')
        plt.xlabel('std dev ADC')
        plt.ylabel('channel count')
        plt.savefig(f"plots/{runNo}_std.png", transparent=True)
        plt.close()

        fig = plt.figure()
        plt.hist(list(map(lambda x: x[1], out)), bins=200, histtype='step')
        plt.yscale('log', nonposy='clip')
        plt.xlabel('mean ADC')
        plt.ylabel('channel count')
        plt.savefig(f"plots/{runNo}_mean_log.png", transparent=True)
        plt.close()

        fig = plt.figure()
        plt.hist(list(map(lambda x: x[2], out)), bins=200, histtype='step')
        plt.yscale('log', nonposy='clip')
        plt.xlabel('std dev ADC')
        plt.ylabel('channel count')
        plt.savefig(f"plots/{runNo}_std_log.png", transparent=True)
        plt.close()

        fig = plt.figure()
        plt.figure()
        plt.scatter(list(map(lambda x: x[1], out)), list(map(lambda x: x[2], out)))
        plt.xlabel('mean ADC')
        plt.ylabel('std dev ADC')
        plt.savefig(f"plots/{runNo}_meanStd.png", transparent=True)
        plt.close()

    plt.figure(1)
    plt.legend(loc='upper right')
    plt.savefig(f"plots/cum_mean.png", transparent=True)
    plt.xlabel('mean ADC')
    plt.ylabel('channel count')
    plt.close()

    plt.figure(2)
    plt.legend(loc='upper right')
    plt.yscale('log', nonposy='clip')
    plt.xlabel('mean ADC')
    plt.ylabel('channel count')
    plt.savefig(f"plots/cum_mean_log.png", transparent=True)
    plt.close()

    plt.figure(3)
    plt.legend(loc='upper right')
    plt.xlabel('std dev ADC')
    plt.ylabel('channel count')
    plt.savefig(f"plots/cum_std.png", transparent=True)
    plt.close()

    plt.figure(4)
    plt.legend(loc='upper right')
    plt.yscale('log', nonposy='clip')
    plt.xlabel('std dev ADC')
    plt.ylabel('channel count')
    plt.savefig(f"plots/cum_std_log.png", transparent=True)
    plt.close()





if __name__ == '__main__':
    distributionPlots(sys.argv[1])
