# Discrete Grid System Tiler (DGGS)
Utility for building and querying Discrete Grid Systems.  Supports both [Discrete Global Grid Systems](http://www.opengeospatial.org/projects/groups/dggsswg) (DGGS) and Local Grid Systems (LGS).


## Usage
#### Python
```python
from dggs import DistanceConfiguration
from dggs import DGGS

extent = [-100, 100, -50, 50] #[xmin, xmax, ymin, ymax] bounds
epsg = 4326 #Interpret units as WGS84
x_spacing = 1 #1 degree grid spacing
y_spacing = 1 #1 degree grid spacing

#Build the configuration
dggs_config = DistanceConfiguration(extent, x_spacing, y_spacing, epsg)

#Build DGGS:
point_grid = DGGS(dggs_config).PointGrid() #Point grid
box_grid = DGGS(dggs_config).BoxGrid() #Rectangular grid cells
hexgon_grid = DGGS(dggs_config).HexagonGrid() #Hexagonal grid cells
```


#### Command Line
Command line script for deploying a DGGS as a cloud optimized vector from a JSON configuration file.
```bash
dggs config.json
```

##### config.json
```json
{"extent": [-3.5,3.5,-1.0,1.0],
 "spacing": {"horizontal": 1,
             "vertical": 1,
             "mode": "distance",
             "xoverlap": 0,
             "yoverlap": 0
             },
 "epsg": 4326,
 "grid_type": "Hexagon",
 "precision": 12,
 "bucket": "bucket",
 "key": "key",
 "multi": "True",
 "metadata": "True"
 }
```