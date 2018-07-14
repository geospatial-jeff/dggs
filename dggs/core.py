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

    def PointGrid(self):
        columns, rows = self.config.dimensions

        centroid_list = []

        for col in range(columns):
            for row in range(rows):
                x = self.config.extent[0] + (col * self.h_spacing - col * self.config.h_overlap)
                y = self.config.extent[3] - (row * self.v_spacing - row * self.config.v_overlap)
                centroid_list.append([x,y])
        return PointDGGS(centroid_list, self.config.epsg)

class PointDGGS():

    """Class containing functionality for Point DGGS"""

    def __init__(self, centroid_list, epsg):
        self.centroids = centroid_list
        self.epsg = epsg