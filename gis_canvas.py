# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5


def points_to_QgsLine(points_list):
    return qgis.core.QgsGeometry.fromPolyline(
        [qgis.core.QgsPoint(x, y) for x, y in points_list]
    )


def points_to_simple_QgsPolygon(points_list):
    return qgis.core.QgsGeometry.fromPolygonXY([
        [qgis.core.QgsPointXY(x, y) for x, y in points_list]
    ])


class Gis_Canvas(qgis.gui.QgsMapCanvas):
    def __init__(self, parent):
        super(Gis_Canvas, self).__init__(parent)
        self.setVisible(True)
        self.set_projection('EPSG:4326')  # 设置显示投影(4326:wgs84经纬坐标直接投影)
        self.base_map_layers = []
        self.mission_layers = []
        self.load_online_map('openstreetmap')
        # self.test_add_geometry()
        self.test_load_shapefile()
        self.zoom_to_china()
        self.refresh()
        self.init_member_widgets()
        self.refresh()

    def init_member_widgets(self):
        self.mouse_location_label = PyQt5.QtWidgets.QLabel(self)
        self.mouse_location_label.move(0, 0)
        self.mouse_location_label.resize(300, 20)

    def mousePressEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            self.press_location = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
        super(Gis_Canvas, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        mouse_map_coordinates = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())

        self.mouse_location_label.setText('x: %.3f  y: %.3f' % (mouse_map_coordinates.x(), mouse_map_coordinates.y()))  # 显示鼠标位置

        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            if 'press_location' in dir(self):
                self.setCenter(qgis.core.QgsPointXY(
                    self.center().x() - mouse_map_coordinates.x() + self.press_location.x(),
                    self.center().y() - mouse_map_coordinates.y() + self.press_location.y()))
                self.refresh()

        super(Gis_Canvas, self).mouseMoveEvent(event)

    '''
    加载在线WMS地图
    '''
    def load_online_map(self, source):
        service_uri = ''
        if source == 'openstreetmap':
            url = 'a.tile.openstreetmap.org/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db'
            service_uri = "type=xyz&zmin=0&zmax=19&url=http://" + url
        elif source == 'openstreetmap_cycle':
            url = 'tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=99d9c81a71684632866e776b7a9035db'
            service_uri = "type=xyz&zmin=0&zmax=19&url=http://" + url
        else:
            raise 'unknown online map source %s' % str(source)
        new_base_map_layer = qgis.core.QgsRasterLayer(service_uri, 'base_map', 'wms')
        for old_base_map_layer in self.base_map_layers:
            qgis.core.QgsProject.instance().removeMapLayer(old_base_map_layer)
        self.base_map_layers = [new_base_map_layer]
        qgis.core.QgsProject.instance().addMapLayer(new_base_map_layer, True)
        self.setLayers(self.mission_layers + self.base_map_layers)
        self.refresh()

    '''
    设置显示投影
    '''
    def set_projection(self, epsg_code='4326'):
        self.setDestinationCrs(qgis.core.QgsCoordinateReferenceSystem(epsg_code))

    def test_load_shapefile(self):
        import platform
        sys_name = platform.system().lower()
        shapefile_name = ''
        if sys_name.startswith('darwin'):  # mac
            shapefile_name = '/Applications/QGIS3.app/Contents/Resources/resources/data/world_map.shp'
        elif sys_name.startswith('win'):  # windows
            shapefile_name = 'C:/Program Files/QGIS 3.6/apps/qgis/resources/data/world_map.shp'
        else:
            raise 'unknown system'
        shapefile_layer = qgis.core.QgsVectorLayer(shapefile_name, 'world_map_from_shapefile', 'ogr')
        qgis.core.QgsProject.instance().addMapLayer(shapefile_layer, True)
        self.mission_layers = [shapefile_layer] + self.mission_layers
        self.setLayers(self.mission_layers + self.base_map_layers)
        self.refresh()

    def show_temp_polyline_from_points_list(self,
                                           points_list,
                                           epsgcode,
                                           color=PyQt5.QtCore.Qt.black,
                                           width=3,
                                           line_style=PyQt5.QtCore.Qt.SolidLine, #DashLine, DotLine, DashDotLine, DashDotDotLine
                                           ):
        poly = qgis.gui.QgsRubberBand(self, False)
        poly.setToGeometry(points_to_QgsLine(points_list), None)
        poly.setColor(color)
        poly.setWidth(width)
        poly.setLineStyle(line_style)
        poly.show()

    def show_temp_polygon_from_points_list(self, points_list, epsgcode):
        poly = qgis.gui.QgsRubberBand(self)
        poly.setToGeometry(points_to_simple_QgsPolygon(points_list), None)
        poly.setColor(PyQt5.QtGui.QColor(0, 0, 255))
        poly.setFillColor(PyQt5.QtGui.QColor(255,255,0))
        poly.setWidth(3)
        poly.show()

    def add_polygon_layer_from_points_list(self, points_list, epsgcode):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:%s&field=fldtxt:string" % epsgcode, "layer", "memory")
        f = qgis.core.QgsFeature()
        g = points_to_simple_QgsPolygon(points_list)
        f.setGeometry(g)
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def add_polygon_layer_from_wkt(self, wkt_str, epsgcode):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:%s&field=fldtxt:string" % epsgcode, "layer", "memory")
        f = qgis.core.QgsFeature()
        geo = qgis.core.QgsGeometry.fromWkt(wkt_str)
        f.setGeometry(geo)
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def test_add_geometry(self):
        layer = qgis.core.QgsVectorLayer("Polygon?crs=epsg:4326&field=fldtxt:string", "layer", "memory")
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(15, 31, 18, 33)))
        layer.dataProvider().addFeatures([f])
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(30, 20, 50, 80)))
        layer.dataProvider().addFeatures([f])
        f = qgis.core.QgsFeature()
        f.setGeometry(qgis.core.QgsGeometry.fromRect(qgis.core.QgsRectangle(156.71, 50.93, 156.72, 50.94)))
        layer.dataProvider().addFeatures([f])
        qgis.core.QgsProject.instance().addMapLayer(layer, True)
        self.setLayers([layer] + self.layers())

    def zoom_to_rectangle(self, min_x, min_y, max_x, max_y):
        self.setExtent(qgis.core.QgsRectangle(min_x, min_y, max_x, max_y))
        self.refresh()

    def zoom_to_china(self):
        self.zoom_to_rectangle(74, 10, 135, 54)

    def zoom_to_pku(self):
        self.zoom_to_rectangle(116.294, 39.980, 116.315, 40)


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.canvas = Gis_Canvas(self)
        self.main_layout.addWidget(self.canvas)

        self.button= PyQt5.QtWidgets.QPushButton(self)
        self.main_layout.addWidget(self.button)
        self.button.clicked.connect(self.onClick)

        self.fix_screen_resolution()
    
    def fix_screen_resolution(self, percentage=0.9):
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*percentage, screenRect.height()*percentage)

    def onClick(self):
        print('ok')
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*0.8, screenRect.height()*0.8)
        self.canvas.zoom_to_china()



if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
