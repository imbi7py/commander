import PyQt5.QtCore, time, threading, qgis.gui, qgis.core

class Point_Simulation():
    def __init__(self, rc, start_position):
        self.rc = rc

        self.label = PyQt5.QtWidgets.QLabel(self.rc.gis_canvas)
        self.label.show()
        self.label.resize(50, 50)
        self.label.setText('plane')
        self.move_label_to_geo_point(start_position[0], start_position[1])
    
    def move_label_to_geo_point(self, x, y):
        x, y = self.rc.gis_canvas.to_map_point((x, y), 'EPSG:4326')
        x, y = self.rc.gis_canvas.to_window_point(x, y)
        self.label.move(x-25, y-25)

    def to_map_qgspoint(self, geo_point):
        mapx, mapy = self.rc.gis_canvas.to_map_point(geo_point, 'EPSG:4326')
        return qgis.core.QgsPointXY(mapx, mapy)

    def move_to(self, new_position):
        self.move_label_to_geo_point(new_position[0], new_position[1])

    def hide(self):
        self.label.hide()

class Polyline_Simulation():
    def __init__(self, rc, polyline):
        self.rc = rc
        self.polyline = polyline
    
    def begin(self):
        self.point_simu = Point_Simulation(self.rc, self.polyline[0])
        
        self.simulate_thread = threading.Thread(target = self.run, daemon=True)
        self.simulate_thread.start()
    
    def run(self):
        for point in self.polyline:
            self.point_simu.move_to(point)
            time.sleep(0.1)
        self.point_simu.hide()