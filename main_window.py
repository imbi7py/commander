# coding:utf-8
import os, sys, logging, functools
import mysql.connector
import load_libs
import PyQt5
import resource_context
import quickview_monitor
import gis_canvas
import mission_widget

class Commonder_Main(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        self.init_resource()

        PyQt5.QtWidgets.QMainWindow.__init__(self)
        PyQt5.uic.loadUi('main_window.ui', self)
        self.init_widgets()
        self.init_actions()
        self.init_language()
        self.resize(1920, 1080)
        self.gis_canvas.zoom_to_pku()

    def init_widgets(self):
        self.init_quickview_monitors_widgets()
        self.init_quickview_monitors_view(2, 2)
        self.init_gis_canvas()
        self.init_mission_widget()
        self.init_view()
        self.init_actions()

    def init_actions(self):
        self.show_history_quickviews.triggered.connect(self.show_history_quickviews_func)
        self.debug.triggered.connect(self.debug_button_click)
        self.zoom_to_china.triggered.connect(self.gis_canvas.zoom_to_china)
        self.use_chinese.triggered.connect(self.init_language)
        self.show_quickview.triggered.connect(self.refresh_widgets_visible)
        self.show_mission.triggered.connect(self.refresh_widgets_visible)
        self.show_map.triggered.connect(self.refresh_widgets_visible)

        self.actionshow_1_quickviews.triggered.connect(functools.partial(self.init_quickview_monitors_view, 1, 1))
        self.actionshow_2_quickviews_h.triggered.connect(functools.partial(self.init_quickview_monitors_view, 2, 1))
        self.actionshow_2_quickviews_v.triggered.connect(functools.partial(self.init_quickview_monitors_view, 1, 2))
        self.actionshow_4_quickviews.triggered.connect(functools.partial(self.init_quickview_monitors_view, 2, 2))
    
    def init_view(self):
        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_vertical_layout = PyQt5.QtWidgets.QHBoxLayout(self)
        self.main_widget.setLayout(self.main_vertical_layout)
        self.setCentralWidget(self.main_widget)
        self.main_vertical_layout.addWidget(self.mission_widget, 1)
        self.main_vertical_layout.addWidget(self.gis_canvas, 2)
        self.main_vertical_layout.addWidget(self.quickview_widget, 2)
        self.refresh_widgets_visible()

    def refresh_widgets_visible(self):
        for x in range(self.quickview_layout.maxcols):
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[y][x].clear_img()

        if self.show_quickview.isChecked():
            self.quickview_widget.show()
        else:
            self.quickview_widget.hide()
        if self.show_mission.isChecked():
            self.mission_widget.show()
        else:
            self.mission_widget.hide()
        if self.show_map.isChecked():
            self.gis_canvas.show()
        else:
            self.gis_canvas.hide()
    
    def init_language(self):
        if self.use_chinese.isChecked():
            self.setWindowTitle('指挥车')

            self.mainmenu_mission.setTitle('任务')

            self.mainmenu_view.setTitle('视图')
            self.show_quickview.setText('显示快视图')
            self.show_map.setText('显示地图')
            self.show_mission.setText('显示任务视图')
            self.use_chinese.setText('use chinese')

            self.mainmenu_map.setTitle('地图控件')
            self.zoom_to_china.setText('缩放至中国')

            self.mainmenu_quickview.setTitle('快视图')
            self.show_history_quickviews.setText('显示历史快视图')
            self.actionshow_1_quickviews.setText('显示1张快视图')
            self.actionshow_2_quickviews_h.setText('水平显示2张快视图')
            self.actionshow_2_quickviews_v.setText('垂直显示2张快视图')
            self.actionshow_4_quickviews.setText('显示4张快视图')

            self.mainmenu_help.setTitle('帮助')
        else:
            self.setWindowTitle('commander')
            self.mainmenu_mission.setTitle('mission')
            self.mainmenu_view.setTitle('view')
            self.show_quickview.setText('show quickview')
            self.show_map.setText('show map')
            self.show_mission.setText('show mission')
            self.use_chinese.setText('中文')

            self.mainmenu_map.setTitle('map')
            self.zoom_to_china.setText('zoom to china')

            self.mainmenu_quickview.setTitle('quickview')
            self.show_history_quickviews.setText('show history quickviews')
            self.actionshow_1_quickviews.setText('show 1 quickviews')
            self.actionshow_2_quickviews_h.setText('show 2 quickviews horizontal')
            self.actionshow_2_quickviews_v.setText('show 2 quickviews vertical')
            self.actionshow_4_quickviews.setText('show 4 quickviews')

            self.mainmenu_help.setTitle('help')

    def debug_button_click(self):
        self.gis_canvas.zoom_to_china()
        self.gis_canvas.refresh()

    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)
    
    def init_mission_widget(self):
        self.mission_widget = mission_widget.Mission_Widget(self, self.rc)

    def init_gis_canvas(self):
        self.gis_canvas = gis_canvas.Gis_Canvas(self, self.rc)
    
    def init_quickview_monitors_widgets(self):
        self.quickview_widget = PyQt5.QtWidgets.QWidget(self)
        self.quickview_layout = PyQt5.QtWidgets.QGridLayout(self)
        self.quickview_widget.setLayout(self.quickview_layout)
        self.quickview_layout.maxrows = 2
        self.quickview_layout.maxcols = 2
        self.quickview_monitors = {}
        self.quickview_monitors_mat = []

        def init_one_quickview_monitor(x, y):
            name = '%d_%d' % (x, y)
            one_monitor = quickview_monitor.Quickview_Monitor(self, self.rc, name)
            self.quickview_monitors[name] = one_monitor
            self.quickview_layout.addWidget(one_monitor, x, y)
            return one_monitor
        for x in range(self.quickview_layout.maxcols):
            self.quickview_monitors_mat.append([])
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[x].append(init_one_quickview_monitor(x, y))

    def init_quickview_monitors_view(self, rows, cols):
        for x in range(self.quickview_layout.maxcols):
            for y in range(self.quickview_layout.maxrows):
                self.quickview_monitors_mat[y][x].clear_img()
                if x < cols and y < rows:
                    self.quickview_monitors_mat[y][x].show()
                else:
                    self.quickview_monitors_mat[y][x].hide()

    def show_realtime_quickview(self, quickview_data):
        for one_monitor in self.quickview_monitors.values():
            one_monitor.check_and_show_quickview(quickview_data)
            

    def show_history_quickviews_func(self):
        quickviews = self.rc.quickview_store.get_all_quickviews()
        for quickview in quickviews:
            img = quickview['img_pil']
            img.show()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = Commonder_Main()
    form.show()
    sys.exit(app.exec_())
