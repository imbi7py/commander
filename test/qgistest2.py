import os, sys, logging
#print (os.environ.get('QGIS_PREFIX_PATH', 'notfound'))
#os.environ['QGIS_PREFIX_PATH'] = 'C:/Program Files/QGIS 3.6/apps/qgis'
#print (os.environ.get('QGIS_PREFIX_PATH', 'notfound'))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import load_libs

import qgis, PyQt5
from qgis.gui import *
#from qgis.PyQt.QtCore import SIGNAL, Qt, QString
from qgis.PyQt.QtWidgets import QMainWindow, QAction
from qgis.core import *

class MyWnd(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        layer = QgsVectorLayer("Polygon?crs=epsg:4326&field=fldtxt:string",
                               "layer", "memory")


        self.canvas = QgsMapCanvas()
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(15, 31, 18, 33)))
        layer.dataProvider().addFeatures([f])
        f2 = QgsFeature()
        f2.setGeometry(QgsGeometry.fromRect(QgsRectangle(30, 20, 50, 80)))
        layer.dataProvider().addFeatures([f2])
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(1, 1, 2, 2)))
        layer.dataProvider().addFeatures([f])
        class mIface(QgisInterface):
            def __init__(self):
                QgisInterface.__init__(self)
                pass
        #iface = mIface()
        #self.canvas.setCanvasColor(PyQt5.QtCore.Qt.green)
        #layer2 = QgsVectorLayer('C:/Users/cjl/Desktop/commander/maps/china/province.shp', 'china_province', 'ogr')
        layer2 = QgsVectorLayer('C:/Users/cjl/Desktop/commander/maps/china_sheng/CN-sheng-A.shp', 'test', 'ogr')
        #layer2 = iface.addVectorLayer('C:/Users/cjl/Desktop/commander/maps/china_sheng/CN-sheng-A.shp', 'CN-sheng-A', 'ogr')
        #layer2 = QgsVectorLayer('C:\\Users\\cjl\\Desktop\\commander\\maps\\china_sheng\\CN-sheng-A.shp', 'china_province', 'ogr')
        #layer2 = QgsVectorLayer('C:\Program Files\QGIS 3.6\apps\qgis\resources\data', 'world_map.shx', 'ogr')
        #layer2 = QgsVectorLayer('C:/Users/cjl/Desktop/commander/maps/china/湖泊河流', 'china_province', 'mapclub')


        print (layer.isValid())
        print (layer2.isValid())
        self.canvas.setLayers([layer])
        print (self.canvas.layers())
        self.canvas.setExtent(QgsRectangle(0, 0, 100, 100))
        l = self.canvas.layers()[0]
        #l.selectAll()
        QgsProject.instance().addMapLayer(l, True)
        QgsProject.instance().addMapLayer(layer2, True)
        #self.canvas.zoomToFullExtent()
        self.canvas.setVisible(True)
        #print (l.boundingBoxOfSelected())
        #self.canvas.show()
        self.canvas.refresh()

        #self.canvas.setExtent(layer.extent())
        #self.canvas.setLayers([layer])

        self.setCentralWidget(self.canvas)
        self.toolbar = self.addToolBar("Canvas actions")

        #self.actionZoomIn = QAction("Zoom in", self)
        #self.actionZoomOut = QAction("Zoom out", self)
        #self.actionPan = QAction("Pan", self)
#
        #self.actionZoomIn.setCheckable(True)
        #self.actionZoomOut.setCheckable(True)
        #self.actionPan.setCheckable(True)
#
        #self.actionZoomIn.triggered.connect(self.zoomIn)
        #self.actionZoomOut.triggered.connect(self.zoomOut)
        #self.actionPan.triggered.connect(self.pan)

        #self.toolbar.addAction(self.actionZoomIn)
        #self.toolbar.addAction(self.actionZoomOut)
        #self.toolbar.addAction(self.actionPan)

        # create the map tools
        #self.toolPan = QgsMapToolPan(self.canvas)
        #self.toolPan.setAction(self.actionPan)
        #self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        #self.toolZoomIn.setAction(self.actionZoomIn)
        #self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        #self.toolZoomOut.setAction(self.actionZoomOut)

        #self.pan()

logging.basicConfig(level=logging.DEBUG)
os.environ["GDAL_DATA"] = 'C:/Program Files/QGIS 3.6/share/gdal'
#print (QgsApplication.prefixPath())
QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.6/apps/qgis", True)
#print (QgsApplication.prefixPath())
print (QgsApplication.showSettings())
app = PyQt5.QtWidgets.QApplication(sys.argv)
#app.initQgis()
form = MyWnd()
form.show()
sys.exit(app.exec_())
    #def zoomIn(self):
    #    self.canvas.setMapTool(self.toolZoomIn)
#
    #def zoomOut(self):
    #    self.canvas.setMapTool(self.toolZoomOut)
#
    #def pan(self):
    #    self.canvas.setMapTool(self.toolPan)