import multiprocessing
from multiprocessing import Pool
import functools
import geohash
from pyproj import Proj, transform
import json



class DGGS():

    def __init__(self, config):
        self.config = config
        self.h_spacing, self.v_spacing = config.spacing
        self.cols, self.rows = self.config.dimensions