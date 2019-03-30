# coding:utf-8
import os, sys, logging
import mysql.connector
import load_libs
import PyQt5
import resource_context
import quickview_monitor
import gis_canvas

class Add_Area_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent, rc):
        PyQt5.QtWidgets.QDialog.__init__(self, parent)
        PyQt5.uic.loadUi('add_area_dialog.ui', self)
        self.rc = rc
        self.reDraw.clicked.connect(self.start_draw)
        self.polygon = None
        self.start_draw()
    
    def start_draw(self):
        if 'polygon_rubber_band' in dir(self):
            self.polygon_rubber_band.hide()
            del(self.polygon_rubber_band)
        self.rc.gis_canvas.start_draw_polygon(self.draw_finished)
    
    def draw_finished(self, polygon):
        self.polygon = polygon
        self.coors_label.setText(str(self.polygon))
        self.rc.gis_canvas.stop_draw_polygon()
        self.polygon_rubber_band = self.rc.gis_canvas.show_temp_polygon_from_points_list(self.polygon, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.yellow)
    
    def accept(self):
        if self.polygon is None:
            PyQt5.QtWidgets.QMessageBox.critical(self, 'ERROR', 'ERROR: please draw a polygon')
        else:
            area_name = self.area_name_textedit.toPlainText()
            area_polygon = self.polygon
            success, ret = self.rc.mission_manager.add_area(area_name, area_polygon)
            if not success:
                PyQt5.QtWidgets.QMessageBox.critical(self, 'ERROR', 'ERROR: %s' % ret)
            else:
                self.polygon_rubber_band.hide()
                del(self.polygon_rubber_band)
                self.close()

class Mission_Widget_Item(PyQt5.QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, rc, type_, binding_object):
        PyQt5.QtWidgets.QTreeWidgetItem.__init__(self, parent)
        self.parent = parent
        self.rc = rc
        self.type = type_
        self.binding_object = binding_object
        self.setText(0, binding_object.name)
        self.attribute = []
    
    def get_right_click_menu(self):
        menu = PyQt5.QtWidgets.QMenu(self.rc.main_window)
        if self.type == 'area':
            menu_item = menu.addAction('添加飞行任务')
            menu_item.triggered.connect(lambda: print('TODO 完成添加飞行任务'))
            menu_item = menu.addAction('删除观测区域')
            menu_item.triggered.connect(lambda: print('TODO 删除观测区域'))
        return menu

class Mission_Widget(PyQt5.QtWidgets.QTreeWidget):
    def __init__(self, main_window, rc):
        PyQt5.QtWidgets.QTreeWidget.__init__(self, main_window)
        self.rc = rc
        self.rc.mission_widget = self
        self.setHeaderLabels(['所有飞行区域'])

    def mousePressEvent(self, event):
        if event.buttons() == PyQt5.QtCore.Qt.RightButton:
            item = self.itemAt(event.pos())
            if item:
                menu = item.get_right_click_menu()
                menu.move(event.globalPos())
                menu.show()
            else:
                menu = self.get_right_click_menu()
                menu.move(event.globalPos())
                menu.show()
        super(Mission_Widget, self).mousePressEvent(event)
    
    def get_right_click_menu(self):
        menu = PyQt5.QtWidgets.QMenu(self)
        menu_item = menu.addAction('添加飞行区域')
        menu_item.triggered.connect(self.add_area_dialog)
        return menu
    
    def add_area_dialog(self):
        dialog = Add_Area_Dialog(self.rc.main_window, self.rc)
        dialog.move(self.mapToGlobal(self.pos()))
        dialog.show()
    
    def add_area(self, area_object):
        area_item = Mission_Widget_Item(self, self.rc, 'area', area_object)
        area_item.setExpanded(True)
        return area_item

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
        self.init_quickview_monitors()
        self.init_gis_canvas()
        self.init_mission_widget()
        self.init_view()
        self.init_actions()

    def init_actions(self):
        self.show_history_quickviews.triggered.connect(self.show_history_quickviews_func)
        self.debug.triggered.connect(self.debug_button_click)
        self.zoom_to_china.triggered.connect(self.gis_canvas.zoom_to_china)
        self.use_chinese.triggered.connect(self.init_language)
        self.show_quickview.triggered.connect(self.reset_main_vertical_layout)
        self.show_mission.triggered.connect(self.reset_main_vertical_layout)
    
    def init_view(self):
        self.main_widget = PyQt5.QtWidgets.QWidget(self)
        self.main_vertical_layout = PyQt5.QtWidgets.QHBoxLayout(self)
        self.main_widget.setLayout(self.main_vertical_layout)
        self.setCentralWidget(self.main_widget)
        self.reset_main_vertical_layout()
    
    def reset_main_vertical_layout(self):
        for i in range(self.main_vertical_layout.count()):
            self.main_vertical_layout.removeItem(
                self.main_vertical_layout.itemAt(0)
            )
        if self.show_quickview.isChecked():
            self.main_vertical_layout.addLayout(self.quickview_layout, 2)
        if self.show_mission.isChecked():
            self.main_vertical_layout.addWidget(self.mission_widget, 1)
        self.main_vertical_layout.addWidget(self.gis_canvas, 2)
    
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

            self.mainmenu_help.setTitle('help')

    def debug_button_click(self):
        self.gis_canvas.zoom_to_china()
        self.gis_canvas.refresh()

    def init_resource(self):
        self.rc = resource_context.ResourceContext()
        self.rc.init_resources(self)
    
    def init_mission_widget(self):
        self.mission_widget = Mission_Widget(self, self.rc)

    def init_gis_canvas(self):
        self.gis_canvas = gis_canvas.Gis_Canvas(self, self.rc)

    def init_quickview_monitors(self):
        self.quickview_layout = PyQt5.QtWidgets.QGridLayout(self)
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
