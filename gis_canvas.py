# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5


class Gis_Canvas(qgis.gui.QgsMapCanvas):
    def __init__(self, parent):
        qgis.gui.QgsMapCanvas.__init__(self, parent)
        self.setVisible(True)
        self.set_projection('EPSG:4326')  # 设置显示投影(4326:wgs84经纬坐标直接投影)
        self.base_map_layers = []
        self.mission_layers = []
        #self.load_online_map('openstreetmap')
        #self.test_add_geometry()
        self.test_load_shapefile()
        self.zoom_to_china()
        self.refresh()

    '''
    加载在线WMS地图
    '''
    def load_online_map(self, source='openstreetmap'):
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
    def set_projection(self, epsg_code='EPSG:4326'):
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

    def zoom_to_china(self):
        self.setExtent(qgis.core.QgsRectangle(74, 10, 135, 54))


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 1000)
        self.canvas = Gis_Canvas(self)
        self.canvas.resize(1000, 1000)
        self.canvas.move(0, 0)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
