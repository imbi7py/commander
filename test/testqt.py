import os, sys, logging
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import load_qgis_qt

qgis, PyQt5 = load_qgis_qt.get_imported_libs()

app = PyQt5.QtWidgets.QApplication(sys.argv)

class DemoImpl(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)

    @PyQt5.QtCore.pyqtSlot()
    def on_testButton_clicked(self):
        for s in "This is a demo".split(" "):
            self.testList.addItem(s)


form = DemoImpl()
form.show()
sys.exit(app.exec_())
