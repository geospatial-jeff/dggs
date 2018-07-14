
class DGGSConfiguration():

    def __init__(self, extent, h_spacing, v_spacing, epsg, h_overlap=0, v_overlap=0):
        self.extent = extent
        self.h_spacing = h_spacing
        self.v_spacing = v_spacing
        self.h_overlap = h_overlap
        self.v_overlap = v_overlap
        self.epsg = epsg

    @property
    def width(self):
        return float(self.extent[1] - self.extent[0])

    @property
    def height(self):
        return float(self.extent[3] - self.extent[2])