import multiprocessing
from multiprocessing import Pool
import functools
import geohash
from pyproj import Proj, transform
import json
import boto3
import os


from .profiles import Geojson
from .utils import cloud_optimized_vector

s3 = boto3.resource('s3')

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

    def Deploy(self, bucket, key, precision, multi=False, metadata=False):
        #Deploy the vector
        hashes = self.Encode(precision)
        if multi:
            m = Pool(multiprocessing.cpu_count()-1)
            m.map(functools.partial(cloud_optimized_vector, bucket=bucket, key=key), zip(self.centroids, hashes))
        else:
            map(functools.partial(cloud_optimized_vector, bucket=bucket, key=key), zip(self.centroids, hashes))
        #Upload metadata
        x = [x[0] for x in self.centroids]
        y = [y[1] for y in self.centroids]
        if metadata:
            metadata = {'fcount': len(self.centroids),
                        'extent': (min(x), max(x), min(y), max(y)),
                        'epsg': self.epsg,
                        'geohashes': hashes
                        }
            s3.Object(bucket, os.path.join(key, 'metadata.json')).put(Body=json.dumps(metadata))

    def Encode(self, precision):
        if self.epsg != 4326:
            inProj = Proj(init='epsg:{}'.format(self.epsg))
            outProj = Proj(init='epsg:4326')
            centroids = [transform(inProj,outProj,x[0],x[1]) for x in self.centroids]
            return [geohash.encode(x[1], x[0]) for x in centroids]
        return [geohash.encode(x[1], x[0], precision) for x in self.centroids]

    def ExportToGeojson(self):
        return Geojson(self.centroids).MultiPoint()