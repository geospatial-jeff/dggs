from dggs import DistanceConfiguration, PixelConfiguration
from dggs import DGGS

json_config = {'extent': [-3.5,3.5,-1.0,1.0],
               'spacing': {'horizontal': 1,
                           'vertical': 1,
                           'mode': 'distance',
                           'xoverlap': 0,
                           'yoverlap': 0,
                           'xres': None,
                           'yres': None
                           },
               'epsg': 4326,
               'grid_type': 'Hexagon',
               'precision': 12,
               'bucket': 'slingshot-users',
               'key': 'jeff/dggs_json',
               'multi': True,
               'metadata': True
               }


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

def wrapper(json_config):
    config = _buildconfig(json_config)
    dggs_grid = _buildgrid(json_config, config)
    dggs_grid.Deploy(json_config['bucket'], json_config['key'], json_config['precision'],
                     multi=json_config['multi'], metadata=json_config['metadata'])
