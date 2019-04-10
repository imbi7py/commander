# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5


POLYGON_AS_CLOCKWISE = True

def points_to_QgsLine(points_list):
    return qgis.core.QgsGeometry.fromPolyline(
        [qgis.core.QgsPoint(x, y) for x, y in points_list]
    )


def points_to_simple_QgsPolygon(points_list):
    return qgis.core.QgsGeometry.fromPolygonXY([
        [qgis.core.QgsPointXY(x, y) for x, y in points_list]
    ])


class Gis_Canvas(qgis.gui.QgsMapCanvas):
    def __init__(self, parent, rc=None):
        super(Gis_Canvas, self).__init__(parent)
        self.rc = rc
        if self.rc is not None:
            self.rc.gis_canvas = self
        self.setVisible(True)
        self.set_projection('EPSG:4326')  # 设置显示投影(4326:wgs84经纬坐标直接投影)
        self.base_map_layers = []
        self.mission_layers = []
        self.on_draw_polygon = False
        self.load_online_map('openstreetmap')
        # self.test_add_geometry()
        # self.test_load_shapefile()
        self.zoom_to_china()
        self.init_member_widgets()
        self.refresh()

    def init_member_widgets(self):
        self.mouse_location_label = PyQt5.QtWidgets.QLabel(self)
        self.mouse_location_label.move(0, 0)
        self.mouse_location_label.resize(300, 20)
        self.roam_check_box = PyQt5.QtWidgets.QCheckBox(self)
        self.roam_check_box.move(300, 0)
        self.roam_check_box.setText('漫游')
        self.roam_check_box.set_checked = lambda checked: self.roam_check_box.setCheckState(PyQt5.QtCore.Qt.Checked) if checked else self.roam_check_box.setCheckState(PyQt5.QtCore.Qt.Unchecked)
        self.roam_check_box.set_checked(True)

    def to_window_point(self,point):
        center=self.getCoordinateTransform().toMapCoordinates(self.center().x(),self.center().y())
        point_window_x=self.center().x()+(point.x()-center.x())/self.mapUnitsPerPixel()
        point_window_y=self.center().y()-(point.y()-center.y())/self.mapUnitsPerPixel()
        return (point_window_x, point_window_y)
    
    def start_draw_polygon(self, handler_func):
        self.on_draw_polygon = True
        self.handler_func = handler_func
        self.reset_drawing_polygon()
        self.roam_check_box.set_checked(False)
    
    def reset_drawing_polygon(self):
        self.on_draw_polygon_points=[]
        if 'poly' in dir(self):
            self.poly.hide()
            del(self.poly)
        self.poly = qgis.gui.QgsRubberBand(self)
    
    def add_draw_polygon_point(self, new_point_map_location):
        assert self.on_draw_polygon
        self.on_draw_polygon_points.append(
            (new_point_map_location.x(), new_point_map_location.y()))
    
    def on_draw_polygon_mouse_move(self, new_mouse_location):
        assert self.on_draw_polygon
        if len(self.on_draw_polygon_points) > 0:
            self.poly.hide()
            del(self.poly)
            poly_to_show = self.on_draw_polygon_points + \
                [(new_mouse_location.x(), new_mouse_location.y())] + \
                self.on_draw_polygon_points[:1]
            self.poly = self.show_temp_polyline_from_points_list(poly_to_show, 'EPSG:4326')
            self.refresh()
    
    def finish_draw_a_polygon(self):
        if len(self.on_draw_polygon_points) > 3:
            transfer_points_list=self.clockwise_on_draw_points(self.on_draw_polygon_points)
            if not POLYGON_AS_CLOCKWISE:
                transfer_points_list.reverse()
            self.handler_func(transfer_points_list)
        self.reset_drawing_polygon()

    def stop_draw_polygon(self):
        self.on_draw_polygon = False
        self.reset_drawing_polygon()
        self.roam_check_box.set_checked(True)

    def mousePressEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            self.press_location = mouse_map_location = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
            if self.on_draw_polygon:
                self.add_draw_polygon_point(mouse_map_location)
        elif event.buttons() == PyQt5.QtCore.Qt.RightButton:
            if self.on_draw_polygon:
                self.reset_drawing_polygon()

        super(Gis_Canvas, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.on_draw_polygon==True:
            self.finish_draw_a_polygon()
        super(Gis_Canvas, self).mouseDoubleClickEvent(event)


    def mouseMoveEvent(self, event):
        mouse_map_coordinates = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())

        self.mouse_location_label.setText('x: %.3f  y: %.3f' % (mouse_map_coordinates.x(), mouse_map_coordinates.y()))  # 显示鼠标位置

        if self.on_draw_polygon:
            self.on_draw_polygon_mouse_move(mouse_map_coordinates)

        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            if self.roam_check_box.isChecked() and 'press_location' in dir(self):
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

    def show_temp_polyline_from_points_list( \
            self,
            points_list,
            epsgcode=None,
            color=PyQt5.QtCore.Qt.black,
            width=10,
            line_style=PyQt5.QtCore.Qt.SolidLine, #DashLine, DotLine, DashDotLine, DashDotDotLine
                ):
        poly = qgis.gui.QgsRubberBand(self, qgis.core.QgsWkbTypes.LineGeometry)
        poly.setToGeometry(points_to_QgsLine(points_list), None)
        poly.setColor(color)
        poly.setWidth(width)
        poly.setLineStyle(line_style)
        poly.show()
        return poly

    def show_temp_points_from_points_list(self, points_list, epsgcode=None, width=1, color=PyQt5.QtCore.Qt.black):
        poly = qgis.gui.QgsRubberBand(self, qgis.core.QgsWkbTypes.PointGeometry)
        for x, y in points_list:
            poly.addPoint(qgis.core.QgsPointXY(x, y))
        poly.setColor(color)
        poly.setWidth(width)
        poly.show()
        return poly

    def show_temp_polygon_from_points_list(self, points_list, epsgcode=None, width=1, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.yellow):
        poly = qgis.gui.QgsRubberBand(self)
        poly.setToGeometry(points_to_simple_QgsPolygon(points_list), None)
        poly.setColor(edgecolor)
        poly.setFillColor(fillcolor)
        poly.setWidth(width)
        poly.show()
        return poly

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

    def clockwise_on_draw_points(self,points):
        n=0
        x_min_value=points[0][0]
        y_value=points[0][1]
        length=len(points)
        for i in range(length):
            if points[i][0]<x_min_value:
                n=i
                x_min_value=points[i][0]
            elif points[i][0]==x_min_value:
                if points[i][1]>y_value:
                    n = i
                    x_min_value = points[i][0]
                    y_value=points[i][1]
        #作差积，判断多边形为顺时针还是逆时针
        x1=points[n][1]-points[(n-1+length)%length][0]
        y1=points[n][1]-points[(n-1+length)%length][1]
        x2 = points[(n + 1) % length][0] - points[n][0]
        y2 = points[(n + 1) % length][1] - points[n][1]
        vector=x1*y2-x2*y1
        points_list=[]
        for point in points:
            points_list.append((point[0],point[1]))
        if(vector>0):
            points_list.reverse()
        return points_list


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)

        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_layout = PyQt5.QtWidgets.QVBoxLayout(self)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.canvas = Gis_Canvas(self)
        self.main_layout.addWidget(self.canvas)
        self.drawed_polygon = []
        self.drawed_polygon_rubber_band = []


        #设置button布局
        self.hbox = PyQt5.QtWidgets.QHBoxLayout()
        self.gridGroupBox= PyQt5.QtWidgets.QGroupBox('')
        self.button_layout = PyQt5.QtWidgets.QGridLayout()
        self.button_layout.setSpacing(5)
        self.gridGroupBox.setLayout(self.button_layout)
        self.hbox.addWidget(self.gridGroupBox)

        self.to_china_button = PyQt5.QtWidgets.QPushButton('移动到中国',self)
        self.button_layout.addWidget(self.to_china_button,0,0)
        self.to_china_button.clicked.connect(self.to_china_click)

        self.start_draw_button=PyQt5.QtWidgets.QPushButton('开始绘制多边形',self)
        self.button_layout.addWidget(self.start_draw_button,0,1)
        self.start_draw_button.clicked.connect(self.start_draw_click)

        self.stop_draw_button = PyQt5.QtWidgets.QPushButton('结束绘制多边形', self)
        self.button_layout.addWidget(self.stop_draw_button,0,2)
        self.stop_draw_button.clicked.connect(self.stop_draw_click)

        self.clean_current_button = PyQt5.QtWidgets.QPushButton('删除当前多边形', self)
        self.button_layout.addWidget(self.clean_current_button, 0, 3)
        self.clean_current_button.clicked.connect(self.clean_current_click)

        self.clean_all_button = PyQt5.QtWidgets.QPushButton('删除所有多边形', self)
        self.button_layout.addWidget(self.clean_all_button, 0, 4)
        self.clean_all_button.clicked.connect(self.clean_all_click)

        self.main_layout.addLayout(self.hbox)
        self.fix_screen_resolution()

    
    def fix_screen_resolution(self, percentage=0.9):
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        self.resize(screenRect.width()*percentage, screenRect.height()*percentage)

    def to_china_click(self):
        self.canvas.zoom_to_china()

    def draw_polygon_handler_func(self, one_polygon):
        self.drawed_polygon.append([one_polygon])
        self.drawed_polygon_rubber_band.append(
            self.canvas.show_temp_polygon_from_points_list(one_polygon, 'EPSG:4326'))
        self.canvas.show_temp_points_from_points_list(one_polygon, width=100)

    def start_draw_click(self):
        self.canvas.start_draw_polygon(self.draw_polygon_handler_func)

    def stop_draw_click(self):
        self.canvas.stop_draw_polygon()

    def clean_current_click(self):
        if len(self.drawed_polygon):
            self.drawed_polygon_rubber_band[-1].hide()
            del(self.drawed_polygon[-1])
            del(self.drawed_polygon_rubber_band[-1])

    def clean_all_click(self):
        for i in range(len(self.drawed_polygon)):
            self.drawed_polygon_rubber_band[-1].hide()
            del(self.drawed_polygon[-1])
            del(self.drawed_polygon_rubber_band[-1])

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
