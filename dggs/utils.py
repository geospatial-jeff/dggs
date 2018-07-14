import boto3
import os
import json

from .profiles import Geojson

s3 = boto3.resource('s3')

def cloud_optimized_vector(package, bucket, key):
    data, hashes = package
    geoj = Geojson(data).Point()
    s3.Object(bucket, os.path.join(key, hashes+'.geojson')).put(Body=json.dumps(geoj))
