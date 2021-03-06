import math

from .profiles import Geojson
from .utils import deploy, upload_metadata, encode
from .query import DGGSQuery

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

    def BoxGrid(self):
        box_list = []
        point_grid = self.PointGrid()
        for item in point_grid.centroids:
            #Calculate max/min for each box
            xmin = item[0]
            xmax = item[0] + self.h_spacing
            ymin = item[1] - self.v_spacing
            ymax = item[1]
            #Convert into polygon
            poly = [[xmin, ymax],[xmax, ymax],[xmax, ymin],[xmin, ymin],[xmin, ymax]]
            box_list.append([poly])
        return BoxDGGS(box_list, point_grid.centroids, self.config.epsg, self.h_spacing, self.v_spacing)

    def HexagonGrid(self):
        hexagon_list = []
        centroid_list = []

        #To preserve symmetry, hspacing is fixed relative to vspacing
        x_vertex_low = 0.288675134594813 * self.v_spacing
        x_vertex_high = 0.577350269189626 * self.v_spacing
        h_spacing = x_vertex_low + x_vertex_high

        h_overlap = h_spacing - self.config.h_overlap

        v_spacing_half = self.v_spacing/2.0

        columns = int(math.ceil(float(self.config.extent[1] - self.config.extent[0]) / h_overlap))
        rows = int(math.ceil(float(self.config.extent[3] - self.config.extent[2]) / (self.v_spacing - self.config.v_overlap)))

        for col in range(columns):
            x1 = self.config.extent[0] + (col * h_overlap)
            x2 = x1 + (x_vertex_high - x_vertex_low)
            x3 = self.config.extent[0] + (col * h_overlap) + h_spacing
            x4 = x3 + (x_vertex_high - x_vertex_low)

            for row in range(rows):
                if (col % 2) == 0:
                    y1 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 0) * v_spacing_half) #high
                    y2 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 1) * v_spacing_half) #mid
                    y3 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 2) * v_spacing_half) #low
                else:
                    y1 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 1) * v_spacing_half) #high
                    y2 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 2) * v_spacing_half) #mid
                    y3 = self.config.extent[2] + (row * self.config.v_overlap) - (((row * 2) + 3) * v_spacing_half) #low
                hexagon = [[x1,y2],[x2,y1],[x3,y1],[x4,y2],[x3,y3],[x2,y3],[x1,y2]]
                hexagon_list.append(hexagon)
                cent_x = x1 + (x4 - x1)/2
                cent_y = y3 - (y3-y1)/2
                centroid_list.append([cent_x,cent_y])
        return HexagonDGGS(hexagon_list, centroid_list, self.config.epsg)

class PointDGGS():

    """Class containing functionality for Point DGGS"""

    def __init__(self, centroid_list, epsg):
        self.centroids = centroid_list
        self.epsg = epsg

    def Deploy(self, bucket, key, precision, multi=False, metadata=False):
        hashes = self.Encode(precision)
        deploy(self.centroids, hashes, bucket, key, multi=multi, type='Point')
        if metadata:
            upload_metadata(self.centroids, self.epsg, hashes, bucket, key)
        return DGGSQuery(bucket, key, precision, hashes=hashes)

    def Encode(self, precision):
        return encode(self.centroids, self.epsg, precision)

    def ExportToGeojson(self):
        return Geojson(self.centroids).MultiPoint()

class BoxDGGS():

    def __init__(self, box_list, centroid_list, epsg, v_spacing, h_spacing):
        self.boxes = box_list
        self.epsg = epsg
        self.centroids = centroid_list
        self.v_spacing = v_spacing
        self.h_spacing = h_spacing

    def Encode(self, precision):
        return encode(self.centroids, self.epsg, precision)

    def Deploy(self, bucket, key, precision, multi=False, metadata=False):
        hashes = self.Encode(precision)
        deploy(self.boxes, hashes, bucket, key, multi=multi, type='Polygon')
        if metadata:
            upload_metadata(self.centroids, self.epsg, hashes, bucket, key)
        return DGGSQuery(bucket, key, precision, hashes=hashes)

    def ExportToGeojson(self):
        return Geojson(self.boxes).MultiPolygon()

class HexagonDGGS():

    def __init__(self, hexagon_list, centroid_list, epsg):
        self.hexagons = hexagon_list
        self.centroids = centroid_list
        self.epsg = epsg

    def Encode(self, precision):
        return encode(self.centroids, self.epsg, precision)

    def Deploy(self, bucket, key, precision, multi=False, metadata=False):
        hashes = self.Encode(precision)
        deploy(self.hexagons, hashes, bucket, key, multi=multi, type='Polygon')
        if metadata:
            upload_metadata(self.centroids, self.epsg, hashes, bucket, key)
        return DGGSQuery(bucket, key, precision, hashes=hashes)

    def ExportToGeojson(self):
        return Geojson(self.centroids).MultiPolygon()


