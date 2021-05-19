import yaml
import numpy as np
import sys
import json
import matplotlib.pyplot as plt
import re
from functools import reduce

def _rotate_pixel(pixel_pos, tile_orientation):
    return pixel_pos[0]*tile_orientation[2], pixel_pos[1]*tile_orientation[1]

def unique_channel_id(io_group, io_channel, chip_id, channel_id):
    return channel_id + 64*(chip_id + 256*(io_channel + 256*(io_group)))

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def main(geometry):
    f = open(geometry, 'r')
    geometry_yaml = yaml.load(f, Loader=yaml.FullLoader)

    out = {}

    pixel_pitch = geometry_yaml['pixel_pitch']
    chip_channel_to_position = geometry_yaml['chip_channel_to_position']
    tile_orientations = geometry_yaml['tile_orientations']
    tile_positions = geometry_yaml['tile_positions']
    tpc_centers = geometry_yaml['tpc_centers']
    tile_indeces = geometry_yaml['tile_indeces']
    xs = np.array(list(chip_channel_to_position.values()))[
        :, 0] * pixel_pitch
    ys = np.array(list(chip_channel_to_position.values()))[
        :, 1] * pixel_pitch
    x_size = max(xs)-min(xs)+pixel_pitch
    y_size = max(ys)-min(ys)+pixel_pitch

    for tile in geometry_yaml['tile_chip_to_io']:
        tile_orientation = tile_orientations[tile]

        for chip_channel in geometry_yaml['chip_channel_to_position']:
            chip = chip_channel // 1000
            channel = chip_channel % 1000
            try:
                io_group_io_channel = geometry_yaml['tile_chip_to_io'][tile][chip]
            except KeyError:
                print("Chip %i on tile %i not present in network" % (chip,tile))
                continue

            io_group = io_group_io_channel // 1000
            io_channel = io_group_io_channel % 1000
            x = chip_channel_to_position[chip_channel][0] * \
                pixel_pitch + pixel_pitch / 2 - x_size / 2
            y = chip_channel_to_position[chip_channel][1] * \
                pixel_pitch + pixel_pitch / 2 - y_size / 2

            x, y = _rotate_pixel((x, y), tile_orientation)
            x += tile_positions[tile][2] + \
                tpc_centers[tile_indeces[tile][1]][0]
            y += tile_positions[tile][1] + \
                tpc_centers[tile_indeces[tile][1]][1]

            out[unique_channel_id(io_group, io_channel, chip, channel)] = (x,y)

    f1 = open(geometry[:-5]+"-dict.json", "w")
    f1.write(json.dumps(out))
    f1.close()

if __name__ == '__main__':
    main(sys.argv[1])
