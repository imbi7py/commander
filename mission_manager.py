# coding:utf-8

import PyQt5

class Area():
    def __init__(self, rc, name, polygon):
        self.rc = rc
        self.name = name
        self.polygon = polygon
        self.missions = {}
        self.rubber_band = self.rc.gis_canvas.show_temp_polygon_from_points_list(self.polygon, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.blue)
        self.mission_widget_item = self.rc.mission_widget.add_area(self)
    
    def show(self):
        self.rubber_band.show()
    
    def hide(self):
        self.rubber_band.hide()

class MissionManager():
    def __init__(self, rc):
        self.rc = rc
        self.rc.mission_manager = self
        self.areas = {}
    
    def add_area(self, area_name, area_polygon):
        if area_name in self.areas:
            return False, 'area_name %s alread in areas' % area_name
        
        newarea = Area(self.rc, area_name, area_polygon)
        self.areas[area_name] = newarea
        return True, newarea