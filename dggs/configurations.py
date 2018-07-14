import math

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

class PixelConfiguration(DGGSConfiguration):

    """Class for configuring DGGS where grid size is specified in number of pixels"""

    def __init__(self, extent, h_spacing, v_spacing, epsg, xres, yres, h_overlap=0, v_overlap=0):
        DGGSConfiguration.__init__(self, extent, h_spacing, v_spacing, epsg, h_overlap, v_overlap)
        self.xres = xres
        self.yres = yres

    @property
    def dimensions(self):
        step_x = float(self.h_spacing * self.xres)
        step_y = float(self.v_spacing * self.yres)
        rows = int(round(self.width) / round(step_y))
        cols = int(round(self.height) / round(step_x))
        return (cols, rows)

    @property
    def spacing(self):
        return (float(self.h_spacing * self.xres), float(self.v_spacing * self.yres))