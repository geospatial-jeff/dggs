import boto3
import os
import json
import multiprocessing
from multiprocessing import Pool
import functools
from pyproj import Proj, transform
import geohash

from .profiles import Geojson

s3 = boto3.resource('s3')

def cloud_optimized_vector(package, bucket, key, type):
    data, hashes = package
    geoj = None
    if type == 'Point':
        geoj = Geojson(data).Point()
    elif type == 'Polygon':
        geoj = Geojson(data).Polygon()
    s3.Object(bucket, os.path.join(key, hashes+'.geojson')).put(Body=geoj)


def deploy(data, hashes, bucket, key, multi=False, type='Point'):
    # Deploy the vector
    if multi:
        m = Pool(multiprocessing.cpu_count() - 1)
        m.map(functools.partial(cloud_optimized_vector, bucket=bucket, key=key, type=type),
              zip(data, hashes))
    else:
        map(functools.partial(cloud_optimized_vector, bucket=bucket, key=key, type=type),
            zip(data, hashes))

def upload_metadata(centroids, epsg, hashes, bucket, key):
    x = [x[0] for x in centroids]
    y = [y[1] for y in centroids]
    metadata = {'fcount': len(centroids),
                'extent': (min(x), max(x), min(y), max(y)),
                'epsg': epsg,
                'geohashes': hashes
                }
    s3.Object(bucket, os.path.join(key, 'metadata.json')).put(Body=json.dumps(metadata))

def encode(centroids, epsg, precision):
    centroids = _epsg_check(epsg, centroids)
    return [geohash.encode(x[1], x[0], precision) for x in centroids]

def _epsg_check(epsg, centroids):
    if epsg!= 4326:
        inProj = Proj(init='epsg:{}'.format(epsg))
        outProj = Proj(init='epsg:4326')
        centroids = [transform(inProj, outProj, x[0], x[1]) for x in centroids]
        return centroids
    return centroids


