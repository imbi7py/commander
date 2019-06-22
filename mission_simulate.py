import PyQt5.QtCore, time, threading, qgis.gui, qgis.core, math

class Point_Simulation():
    def __init__(self, rc, start_position):
        self.rc = rc

        self.label = PyQt5.QtWidgets.QLabel(self.rc.gis_canvas)
        self.label.show()
        self.label.resize(50, 50)
        self.label.setText('plane')

        icon_path="pics/icon/aoxiang.png"
        self.icon=PyQt5.QtGui.QPixmap(icon_path)
        self.icon = self.icon.scaled(PyQt5.QtCore.QSize(50, 50))
        self.label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.label.setPixmap(self.icon)
        self.move_label_to_geo_point(start_position[0], start_position[1])
    
    def move_label_to_geo_point(self, x, y):
        x, y = self.rc.gis_canvas.to_map_point((x, y), 'EPSG:4326')
        x, y = self.rc.gis_canvas.to_window_point(x, y)
        self.label.move(x-25, y-25)

    def to_map_qgspoint(self, geo_point):
        mapx, mapy = self.rc.gis_canvas.to_map_point(geo_point, 'EPSG:4326')
        return qgis.core.QgsPointXY(mapx, mapy)

    def move_to(self, new_position, direction_to_east):
        icon_transform=PyQt5.QtGui.QTransform()
        icon_transform.rotate(90 - direction_to_east)
        self.label.setPixmap(self.icon.transformed(icon_transform))
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
        def get_direction_to_east(p1, p2):
            delta_x = p2[0] - p1[0]
            delta_y = p2[1] - p1[1]
            direction = 90.
            if abs(delta_x) < 0.000001:
                if delta_y > 0:
                    direction = 90.
                else:
                    direction = -90
            else:
                direction = math.atan(delta_y / delta_x) / math.pi * 180.
                if delta_x < 0:
                    direction += 180.
            return direction

        for i in range(len(self.polyline)):
            direction = 0.
            if i == len(self.polyline) - 1:
                direction = get_direction_to_east(self.polyline[i-1], self.polyline[i])
            else:
                direction = get_direction_to_east(self.polyline[i], self.polyline[i+1])
            self.point_simu.move_to(self.polyline[i], direction)
            time.sleep(0.2)
        self.point_simu.hide()