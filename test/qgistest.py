import os, sys, logging, platform
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import load_libs

sys_name = platform.system().lower()

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
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(30, 20, 50, 80)))
        layer.dataProvider().addFeatures([f])
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromRect(QgsRectangle(1, 1, 2, 2)))
        layer.dataProvider().addFeatures([f])

        filename = ''
        if sys_name.startswith('darwin'):  # mac
            filename = '/Applications/QGIS3.app/Contents/Resources/resources/data/world_map.shp'
        elif sys_name.startswith('win'):  # windows
            filename = 'C:/Program Files/QGIS 3.6/apps/qgis/resources/data'
        else:
            raise 'unknown system'

        layer2 = QgsVectorLayer(filename, 'test', 'ogr')  # 失败

        print (layer.isValid())
        print (layer2.isValid())  # 如果成功会显实True

        self.canvas.setLayers([layer])
        self.canvas.setExtent(QgsRectangle(0, 0, 100, 100))
        QgsProject.instance().addMapLayer(layer, True)
        self.canvas.setVisible(True)
        self.canvas.refresh()

        self.setCentralWidget(self.canvas)
        self.toolbar = self.addToolBar("Canvas actions")

logging.basicConfig(level=logging.DEBUG)
if sys_name.startswith('darwin'):  # mac
    QgsApplication.setPrefixPath("/Applications/QGIS3.app/Contents/MacOS", True)
elif sys_name.startswith('win'):  # windows
    QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.6/apps/qgis", True)
else:
    raise 'unknown system'

app = PyQt5.QtWidgets.QApplication(sys.argv)
form = MyWnd()
form.show()
sys.exit(app.exec_())