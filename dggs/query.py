import geohash
import os
import boto3
import json

s3 = boto3.resource('s3')

class DGGSQuery():

    def __init__(self, bucket, key, precision, hashes=None):
        self.precision = precision
        self.bucket = bucket
        self.key = key
        if hashes:
            self.hashes = hashes
        else:
            self.hashes = self.RetrieveMetadata()['geohashes']

    def RetrieveObject(self, object):
        contents = s3.Object(self.bucket, os.path.join(self.key, object)).get()['Body'].read().decode('utf-8')
        return json.loads(contents)

    def RetrieveMetadata(self):
        return self.RetrieveObject('metadata.json')

    def Intersects(self, extent, retrieve=False):
        matching_hashes = geohash_bbox_query(extent, self.hashes, self.precision)
        if retrieve:
            return [self.RetrieveObject('{}.geojson'.format(x)) for x in matching_hashes]
        return matching_hashes

#####################################################################################################

def geohash_bbox_query(extent, geohash_list, precision):
    tl_hash = geohash.encode(extent[3], extent[0], precision=precision)
    tr_hash = geohash.encode(extent[3], extent[1], precision=precision)
    br_hash = geohash.encode(extent[2], extent[1], precision=precision)
    bl_hash = geohash.encode(extent[2], extent[0], precision=precision)
    com = common_hash(tl_hash, tr_hash, br_hash, bl_hash)
    intersecting_hashes = [x for x in geohash_list if x.startswith(com)]
    centroids = [geohash.decode(x) for x in intersecting_hashes] #Note these are (y,x)
    return filter_remaining(intersecting_hashes, centroids, extent)

def common_hash(tl_hash, tr_hash, br_hash, bl_hash):
    for item in tl_hash:
        idx = tl_hash.index(item)
        if is_same(tl_hash[idx], tr_hash[idx], br_hash[idx], bl_hash[idx]):
            if idx == len(tl_hash) - 1:
                return tl_hash
            continue
        else:
            return tl_hash[:idx]

def is_same(s1, s2, s3, s4):
    if s1 == s2 == s3 == s4:
        return True
    else:
        return False

def filter_remaining(hashes, centroids, extent):
    valid_list = []
    yspace = y_spacing(centroids)
    xspace = x_spacing(centroids)
    for idx, item in enumerate(hashes):
        if confirm_valid(centroids[idx], extent, yspace, xspace):
            valid_list.append(item)
    return valid_list

def y_spacing(centroids):
    l = centroids.copy()
    first_y = l[0][1]
    while l[0][1] == first_y:
        l.pop(0)
    return abs(first_y - l[0][1])


def x_spacing(centroids):
    return abs(centroids[0][0] - centroids[1][0])

def confirm_valid(centroid, extent, yspace, xspace):
    # print(centroid, extent, yspace, xspace)
    if centroid[1] < extent[1] + xspace and centroid[1] > extent[0] - xspace and centroid[0] < extent[3] + yspace and centroid[0] > extent[2] - yspace:
        return True
    return False