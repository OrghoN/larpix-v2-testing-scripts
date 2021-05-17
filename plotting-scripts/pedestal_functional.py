import h5py
import numpy as np
import sys
import json
from functools import reduce
from collections import defaultdict

_excluded_channels = [6,7,8,9,22,23,24,25,38,39,40,54,55,56,57]

def unique_channel_id(io_group, io_channel, chip_id, channel_id):
    return channel_id + 64*(chip_id + 256*(io_channel + 256*(io_group)))

def getKey(item):
    return item[0]

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def convert(filename):

    print('Opening',filename)
    f = h5py.File(filename,'r')

    data_mask = f['packets'][:]['packet_type'] == 0
    valid_parity_mask = f['packets'][data_mask]['valid_parity'] == 1
    good_data = (f['packets'][data_mask])[valid_parity_mask]

    out = sorted(list(map(lambda x: (unique_channel_id(x['io_group'], x['io_channel'], x['chip_id'], x['channel_id']), x['timestamp'], x['dataword']), good_data)), key=getKey)

    d = defaultdict(list)

    for k, *v in out:
        d[k].append(v)

    out = list(d.items())
    out = list(map(lambda x: [x[0]] + [list(y) for y in zip(*x[1])], out))
    out = list(map(lambda x: (x[0], np.mean(x[2]), np.std(x[2])), out))

    f.close()
    return out

def main(fileList):
    f = open(fileList, "r")

    for file in f:
        f1 = open(file.strip()[:-3]+"-summary.json", "w")
        f1.write(json.dumps(convert(file.strip()), default=np_encoder))
        f1.close()

if __name__ == '__main__':
    main(sys.argv[1])
    # convert(*sys.argv[1:], excluded_channels=_excluded_channels, std_threshold = 4)
