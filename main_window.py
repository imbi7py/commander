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
        self.show_history_quickviews_button.clicked.connect(self.show_history_quickviews)

    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)

    def set_image_to_quickview_label(self, pillow_img):
        self.set_image_to_label(pillow_img, self.label_Quickviewarea)

    def set_image_to_label(self, pillow_img, one_label):
        pillow_img.save('.image_shown_in_image_label.png', 'png')
        one_label.setPixmap(PyQt5.QtGui.QPixmap('.image_shown_in_image_label.png'))

    def show_history_quickviews(self):
        quickviews = self.rc.quickview_store.get_all_quickviews()
        for quickview in quickviews:
            img = quickview['img_pil']
            img.show()

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Commonder_Main()
    form.show()
    sys.exit(app.exec_())
