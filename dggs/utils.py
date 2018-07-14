import boto3
import os
import json

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