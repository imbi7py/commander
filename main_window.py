import os, sys, logging
import mysql.connector
import load_libs
import PyQt5
import resource_context
import quickview_monitor
import gis_canvas


class Commonder_Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        self.init_resource()

        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)
        self.init_quickview_monitors()
        self.init_gis_canvas()

        self.init_actions()

    def init_actions(self):
        self.show_history_quickviews_button.clicked.connect(self.show_history_quickviews)
        self.debugButton.clicked.connect(self.debug_button_click)
        self.zoom_to_china.triggered.connect(self.gis_canvas.zoom_to_china)

    def debug_button_click(self):
        self.gis_canvas.zoom_to_china()
        self.gis_canvas.refresh()

    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)

    def init_gis_canvas(self):
        self.gis_canvas = gis_canvas.Gis_Canvas(self)
        self.gis_layout.addWidget(self.gis_canvas, 0, 0)

    def init_quickview_monitors(self):
        cols = 2
        rows = 2
        self.quickview_monitors = {}

        def init_one_quickview_monitor(x, y):
            name = '%d_%d' % (x, y)
            one_monitor = quickview_monitor.Quickview_Monitor(self, self.rc, name)
            self.quickview_monitors[name] = one_monitor
            self.quickview_layout.addWidget(one_monitor, x, y)
        for x in range(cols):
            for y in range(rows):
                init_one_quickview_monitor(x, y)

    def show_realtime_quickview(self, quickview_data):
        for one_monitor in self.quickview_monitors.values():
            one_monitor.check_and_show_quickview(quickview_data)

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
