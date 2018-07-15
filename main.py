import argparse
import os
import json


from dggs.configurations import PixelConfiguration, DistanceConfiguration
from dggs.core import DGGS

def _config_file(filename):
    try:
        f = open(filename)
        return f
    except FileNotFoundError:
        try:
            print(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename))
            f1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename))
            return f1
        except FileNotFoundError:
            raise ValueError("Could not find the input configuration file: {}".format(filename))

def _buildconfig(json_config):
    spacing = json_config['spacing']
    if spacing['mode'] == 'distance':
        return DistanceConfiguration(json_config['extent'], spacing['horizontal'], spacing['vertical'],
                                     json_config['epsg'], spacing['xoverlap'], spacing['yoverlap'])
    elif spacing['mode'] == 'pixel':
        return PixelConfiguration(json_config['extent'], spacing['horizontal'], spacing['vertical'], json_config['epsg'],
                                  spacing['xres'], spacing['yres'], spacing['xoverlap'], spacing['yoverlap'])

def _buildgrid(json_config, dggs_config):
    dggs_base = DGGS(dggs_config)
    gtype = json_config['grid_type']
    if gtype == 'Point':
        return dggs_base.PointGrid()
    elif gtype == 'Box':
        return dggs_base.BoxGrid()
    elif gtype == 'Hexagon':
        return dggs_base.HexagonGrid()

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    #Check if its a full path:
    data = json.loads(_config_file(args.filename).read())
    config = _buildconfig(data)
    dggs_grid = _buildgrid(data, config)
    dggs_grid.Deploy(data['bucket'], data['key'], data['precision'],
                     multi=data['multi'], metadata=data['metadata'])

if __name__ == "__main__":
    cli()