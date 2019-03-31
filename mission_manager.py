# coding:utf-8

import PyQt5
import mission_widget

class Fly_Mission():
    def __init__(self, rc, name, area, mission_attribute):
        self.rc = rc
        self.name = name
        self.area = area
        self.mission_attribute = mission_attribute
        self.son_mission_widget_items = []
        self.rubber_bands = []
        self.mission_widget_item = self.create_mission_widget_item()
        self.create_rubber_bands()
    
    def create_mission_widget_item(self):
        item = mission_widget.Mission_Widget_Item(
            rc=self.rc,
            parent=self.area.mission_widget_item,
            type_='fly_mission',
            binding_object=self
        )
        item.setExpanded(True)
        return item
    
    def create_polyline_rubber_band(self, name, polyline, color, width, line_style):
        rubber_band = self.rc.gis_canvas.show_temp_polyline_from_points_list(
            polyline,
            color=color, width=width, line_style=line_style)
        rubber_band.name = name
        self.rubber_bands.append(rubber_band)
        item = mission_widget.Mission_Widget_Item(
            rc=self.rc,
            parent=self.mission_widget_item,
            type_='geometry',
            binding_object=rubber_band
        )
        self.son_mission_widget_items.append(item)

    def create_rubber_bands(self):
        self.create_polyline_rubber_band(
            name='任务区域',
            polyline=self.mission_attribute['mission_area']+self.mission_attribute['mission_area'][:1],
            color=PyQt5.QtCore.Qt.red,
            width=1,
            line_style=PyQt5.QtCore.Qt.DashLine)
        self.create_polyline_rubber_band(
            name='航线',
            polyline=self.mission_attribute['shoot_coors_geo'],
            color=PyQt5.QtCore.Qt.blue,
            width=2,
            line_style=PyQt5.QtCore.Qt.SolidLine)
    
    def show(self):
        if 'mission_widget_item' in dir(self):
            if self.mission_widget_item.checkState(0) != PyQt5.QtCore.Qt.Checked:
                self.mission_widget_item.setCheckState(0, PyQt5.QtCore.Qt.Checked)
        for item in self.son_mission_widget_items:
            item.set_checked(True)
    
    def hide(self):
        if 'mission_widget_item' in dir(self):
            if self.mission_widget_item.checkState(0) != PyQt5.QtCore.Qt.Unchecked:
                self.mission_widget_item.setCheckState(0, PyQt5.QtCore.Qt.Unchecked)
        for item in self.son_mission_widget_items:
            item.set_checked(False)

class Area():
    def __init__(self, rc, name, polygon):
        self.rc = rc
        self.name = name
        self.polygon = polygon
        self.missions = {}
        self.rubber_band = self.rc.gis_canvas.show_temp_polygon_from_points_list(self.polygon, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.blue)
        self.mission_widget_item = self.rc.mission_widget.add_area(self)
    
    def show(self):
        if 'mission_widget_item' in dir(self):
            if self.mission_widget_item.checkState(0) != PyQt5.QtCore.Qt.Checked:
                self.mission_widget_item.setCheckState(0, PyQt5.QtCore.Qt.Checked)
        self.rubber_band.show()
    
    def hide(self):
        if 'mission_widget_item' in dir(self):
            if self.mission_widget_item.checkState(0) != PyQt5.QtCore.Qt.Unchecked:
                self.mission_widget_item.setCheckState(0, PyQt5.QtCore.Qt.Unchecked)
        self.rubber_band.hide()
    
    def create_fly_mission(self, mission_attribute):
        newmission_name = mission_attribute['name']
        if newmission_name in self.missions:
            return False, 'ERROR:该区域已有同名任务 %s' % newmission_name
        newmission = Fly_Mission(self.rc, mission_attribute['name'], self, mission_attribute)
        self.missions[newmission_name] = newmission
        self.hide()
        return True, None
        

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