import PyQt5
import PyQt5.QtWidgets ,PyQt5.uic
import os, sys
from PIL import Image

class Login_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, show_main_window_func):
        self.show_main_window_func = show_main_window_func

        PyQt5.QtWidgets.QDialog.__init__(self)
        PyQt5.uic.loadUi('login.ui', self)
        self.label_timu.setPixmap(PyQt5.QtGui.QPixmap('resource/title.PNG'))
        self.label_timu.setScaledContents(True)
        self.label_login.setPixmap(PyQt5.QtGui.QPixmap('resource/log.PNG'))
        self.label_login.setScaledContents(True)
        self.label_ditu.setPixmap(PyQt5.QtGui.QPixmap('resource/ditu.jpg'))
        self.label_ditu.setScaledContents(True)
        self.label_pic.setPixmap(PyQt5.QtGui.QPixmap('resource/pic.png'))
        self.label_pic.setScaledContents(True)


    def accept(self):
        self.show_main_window_func()
        self.close()



if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Login_Dialog(lambda: print('show main window'))
    form.show()
    sys.exit(app.exec_())