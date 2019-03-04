import os, sys, logging
import load_libs
import PyQt5
import resource_context


class Commonder_Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        self.init_resource()

        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)
    
    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)
    
    def add_item_to_list(self, one_item):
        self.testList.addItem(one_item)


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Commonder_Main()
    form.show()
    sys.exit(app.exec_())
