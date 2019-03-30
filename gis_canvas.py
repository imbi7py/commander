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
    def __init__(self, parent,handle):
        super(Gis_Canvas, self).__init__(parent)
        self.setVisible(True)
        self.set_projection('EPSG:4326')  # 设置显示投影(4326:wgs84经纬坐标直接投影)
        self.base_map_layers = []
        self.mission_layers = []
        self.on_draw=False
        self.on_draw_points=[]
        self.handle=handle
        self.poly = qgis.gui.QgsRubberBand(self)
        self.all_temp_layer=[]
        #self.if_finish_polygon=False
        #self.load_online_map('openstreetmap')
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

    def to_window_point(self,point):
        center=self.getCoordinateTransform().toMapCoordinates(self.center().x(),self.center().y())
        point_window_x=self.center().x()+(point.x()-center.x())/self.mapUnitsPerPixel()
        point_window_y=self.center().y()-(point.y()-center.y())/self.mapUnitsPerPixel()
        return (point_window_x, point_window_y)

    def mousePressEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
            self.press_location = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())
            if self.on_draw==True:
                self.on_draw_points.append(self.press_location)
                on_draw_points_window=[]
                for point in self.on_draw_points:
                    on_draw_points_window.append((point.x(),point.y()))
                if len(self.on_draw_points)>0:
                    on_draw_points_window.append((self.on_draw_points[0].x(),self.on_draw_points[0].y()))

                self.hide_temp_polyline_from_points_list(self.poly)
                self.poly=self.show_temp_polyline_from_points_list(on_draw_points_window,'EPSG:4326')
                self.refresh()

        if self.on_draw==True and event.buttons()==PyQt5.QtCore.Qt.RightButton:
            self.on_draw_points = []
            self.hide_temp_polyline_from_points_list(self.poly)
        super(Gis_Canvas, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.on_draw==True:
            self.hide_temp_polyline_from_points_list(self.poly)
            on_draw_polygon_window=[]
            for point in self.on_draw_points:
                on_draw_polygon_window.append((point.x(), point.y()))
            poly=self.show_temp_polygon_from_points_list(on_draw_polygon_window, 'EPSG:4326')
            self.all_temp_layer.append(poly)
            transfer_points_list=self.clickwise_on_draw_points(self.on_draw_points)
            if POLYGON_AS_CLOCKWISE ==False:
                transfer_points_list.reverse()
            self.handle(transfer_points_list)
            self.on_draw_points=[]
            self.refresh()
        super(Gis_Canvas, self).mouseDoubleClickEvent(event)


    def mouseMoveEvent(self, event):
        mouse_map_coordinates = self.getCoordinateTransform().toMapCoordinates(event.x(), event.y())

        self.mouse_location_label.setText('x: %.3f  y: %.3f' % (mouse_map_coordinates.x(), mouse_map_coordinates.y()))  # 显示鼠标位置

        if self.on_draw==True and len(self.on_draw_points)!=0:
            self.hide_temp_polyline_from_points_list(self.poly)
            on_draw_points_window = []
            for point in self.on_draw_points:
                on_draw_points_window.append((point.x(), point.y()))
            on_draw_points_window.append((mouse_map_coordinates.x(),mouse_map_coordinates.y()))
            on_draw_points_window.append((self.on_draw_points[0].x(),self.on_draw_points[0].y()))
            self.poly = self.show_temp_polyline_from_points_list(on_draw_points_window, 'EPSG:4326')
            self.refresh()

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
                                            size=30,
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

    def hide_temp_polyline_from_points_list(self,poly):
        poly.hide()

    def show_temp_polygon_from_points_list(self, points_list, epsgcode):
        poly = qgis.gui.QgsRubberBand(self)
        poly.setToGeometry(points_to_simple_QgsPolygon(points_list), None)
        poly.setColor(PyQt5.QtGui.QColor(0, 0, 255))
        poly.setFillColor(PyQt5.QtGui.QColor(255,255,0))
        poly.setWidth(3)
        poly.show()
        return poly

    def hide_temp_polygon_from_points_list(self,poly):
        poly.hide()

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

    def clickwise_on_draw_points(self,points):
        n=0
        x_min_value=points[0].x()
        y_value=points[0].y()
        length=len(points)
        for i in range(length):
            if points[i].x()<x_min_value:
                n=i
                x_min_value=points[i].x()
            elif points[i].x()==x_min_value:
                if points[i].y()>y_value:
                    n = i
                    x_min_value = points[i].x()
                    y_value=points[i].y()
        #作差积，判断多边形为顺时针还是逆时针
        x1=points[n].x()-points[(n-1+length)%length].x()
        y1=points[n].y()-points[(n-1+length)%length].y()
        x2 = points[(n + 1) % length].x() - points[n].x()
        y2 = points[(n + 1) % length].y() - points[n].y()
        vector=x1*y2-x2*y1
        points_list=[]
        for point in points:
            points_list.append((point.x(),point.y()))
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
        self.handle_func = lambda polygon: print(polygon)

        self.canvas = Gis_Canvas(self,self.handle_func)
        self.main_layout.addWidget(self.canvas)


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
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()  #获取屏幕分辨率
        #self.resize(screenRect.width()*0.8, screenRect.height()*0.8)
        self.canvas.zoom_to_china()

    def start_draw_click(self):
        self.canvas.on_draw = True

    def stop_draw_click(self):
        self.canvas.on_draw = False

    def clean_current_click(self):
        if len(self.canvas.all_temp_layer)>0:
            self.canvas.hide_temp_polygon_from_points_list(self.canvas.all_temp_layer[-1])
        del(self.canvas.all_temp_layer[-1])

    def clean_all_click(self):
        for poly in self.canvas.all_temp_layer:
            self.canvas.hide_temp_polygon_from_points_list(poly)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
