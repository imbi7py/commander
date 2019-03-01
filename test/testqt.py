import logging

qgispath = 'C:/Program Files/QGIS 3.6'
pyqt_plugins = qgispath + '/apps/Qt5/plugins'
qgis_pypath = qgispath + '/apps/qgis/python'
qgis_python_sitepkgspath = qgispath + '/apps/Python37/Lib/site-packages'

def load_qgis():
    try:
        import sys
        sys.path = [qgis_pypath, qgis_python_sitepkgspath] + sys.path
        import PyQt5
        import qgis.core
        import qgis.gui
        return True
    except Exception as e:
        logging.error('load qgis failed')
        logging.exception(e)
        return False

import sys

load_qgis()
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


QApplication.addLibraryPath(pyqt_plugins)
app = QApplication(sys.argv)

class DemoImpl(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('main_window.ui', self)
    
    @pyqtSlot()
    def on_testButton_clicked(self):
        for s in "This is a demo".split(" "):
            self.testList.addItem(s)


form = DemoImpl()
form.show()
sys.exit(app.exec_())