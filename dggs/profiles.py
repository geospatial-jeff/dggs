import json

class Geojson():

    def __init__(self, data, atts=None):
        self.data = data
        self.atts = atts

    def Point(self):
        return json.dumps({"type": "Feature",
                "geometry": {"type": "Point", "coordinates": self.data
                }
            })

    def Line(self):
        return json.dumps({"type": "Feature",
                "geometry": {"type": "LineString", "coordinates": self.data
                }
            })

    def Polygon(self):
        return {"type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": self.data
                }
            }

    def MultiPoint(self):
        return json.dumps({"type": "Feature",
                "geometry": {"type": "MultiPoint", "coordinates": self.data
                }
            })

    def MultiLine(self):
        return json.dumps({"type": "Feature",
                "geometry": {"type": "MultiLineString", "coordinates": self.data
                }
            })

    def MultiPolygon(self):
        return json.dumps({"type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": self.data
                }
            })
