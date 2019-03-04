import os, sys, logging
import load_libs
import PyQt5
import resource_context
from PIL import Image


class Commonder_Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        self.init_resource()

        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)

        self.set_image(Image.open('pics/emojis/0.png'))
    
    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)
    
    def add_item_to_list(self, one_item):
        self.testList.addItem(one_item)
    
    def set_image(self, pillow_img):
        pillow_img.save('.image_shown_in_image_label.png', 'png')
        self.image_label.setPixmap(PyQt5.QtGui.QPixmap('.image_shown_in_image_label.png'))


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Commonder_Main()
    form.show()
    sys.exit(app.exec_())
