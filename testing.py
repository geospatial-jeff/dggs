from dggs import DistanceConfiguration
from dggs import DGGS

config = DistanceConfiguration([-179.99, 179.99, -89.99, 89.99], #extent
                               20, #horizontal spacing
                               20, #vertical spacing
                               4326 #epsg code
                               )



point_grid = DGGS(config).PointGrid()

geojson = point_grid.ExportToGeojson()
geohashes = point_grid.Encode(precision=12)