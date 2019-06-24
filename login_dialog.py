import PyQt5

class Login_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, show_main_window_func):
        self.show_main_window_func = show_main_window_func

        PyQt5.QtWidgets.QDialog.__init__(self)
        PyQt5.uic.loadUi('login.ui', self)
        
    def accept(self):
        self.show_main_window_func()
        self.close()