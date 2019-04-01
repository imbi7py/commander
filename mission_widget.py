# coding:utf-8
import PyQt5
from mission_planning import camera, aerocraft, preload_missions, mission_planning

class Add_Fly_Mission_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent, rc, area_object):
        PyQt5.QtWidgets.QDialog.__init__(self, parent)
        PyQt5.uic.loadUi('add_fly_mission.ui', self)
        self.rc = rc
        self.area_object = area_object
        self.init_data()
        self.camera_attribute_label.setWordWrap(True)
        self.aerocraft_attribute_label.setWordWrap(True)
        self.preload_missions_listwidget.itemSelectionChanged.connect(
            self.preload_mission_selected_changed)
        self.camera_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)
        self.aerocraft_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)
    
    def preload_mission_selected_changed(self):
        selected_mission_name = self.preload_missions_listwidget.selectedItems()[0].text()
        mission_attribute = self.preload_missions[selected_mission_name]
        self.mission_name_textedit.setText(selected_mission_name)
        self.application_textedit.setText(mission_attribute['application'])
        self.camera_cbox.setCurrentText(mission_attribute['cameras'])
        self.aerocraft_cbox.setCurrentText(mission_attribute['aerocraft'])

        self.ground_resolution_m_textedit.setText(str(mission_attribute['ground_resolution_m']))
        self.forward_overlap_textedit.setText(str(mission_attribute['forward_overlap']))
        self.sideway_overlap_textedit.setText(str(mission_attribute['sideway_overlap']))
        if mission_attribute['fly_east_west_direction']:
            self.fly_east_west_checkbox.setCheckState(PyQt5.QtCore.Qt.Checked)
        else:
            self.fly_east_west_checkbox.setCheckState(PyQt5.QtCore.Qt.Unchecked)
    
    def camera_or_aercraft_selected_changed(self):
        self.selected_camera = self.camera_cbox.currentText()
        self.camera_attribute_label.setText(str(self.preload_cameras[self.selected_camera]))
        self.selected_aerocraft = self.aerocraft_cbox.currentText()
        self.aerocraft_attribute_label.setText(str(self.preload_aerocrafts[self.selected_aerocraft]))
    
    def preload_data(self):
        self.preload_missions = preload_missions.missions
        self.preload_cameras = camera.cameras
        self.preload_aerocrafts = aerocraft.aerocrafts
    
    def init_data(self):
        self.preload_data()
        for mission_name in self.preload_missions:
            self.preload_missions_listwidget.addItem(mission_name)
        for camera_name in self.preload_cameras:
            self.camera_cbox.addItem(camera_name)
        for aerocraft_name in self.preload_aerocrafts:
            self.aerocraft_cbox.addItem(aerocraft_name)
        self.preload_missions_listwidget.setCurrentRow(0)
        self.preload_mission_selected_changed()
        self.camera_or_aercraft_selected_changed()
    
    def clear_rubber_band(self):
        if 'polygon_rubber_band' in dir(self):
            self.polygon_rubber_band.hide()
            del(self.polygon_rubber_band)

    def done(self, r):
        PyQt5.QtWidgets.QDialog.done(self, r)
    
    def accept(self):
        params = {
            'area': self.area_object.polygon,
            'mission_name': self.mission_name_textedit.toPlainText(),
            'application': self.application_textedit.toPlainText(),
            'cameras': self.camera_cbox.currentText(),
            'aerocraft': self.aerocraft_cbox.currentText(),
            'fly_east_west_direction': self.fly_east_west_checkbox.isChecked(),
            'ground_resolution_m': self.ground_resolution_m_textedit.toPlainText(),
            'sideway_overlap': self.sideway_overlap_textedit.toPlainText(),
            'forward_overlap': self.forward_overlap_textedit.toPlainText(),
        }
        print('reso', params['ground_resolution_m'])
        succ, ret = mission_planning.mission_planning(
            area_points_list=params['area'],
            mission_name=params['mission_name'],
            aerocraft=params['aerocraft'],
            camera=params['cameras'],
            ground_resolution_m=params['ground_resolution_m'],
            forward_overlap=params['forward_overlap'],
            sideway_overlap=params['sideway_overlap'],
            fly_east_west_direction=params['fly_east_west_direction'],
            application=params['application'],
            )
        if not succ:
            PyQt5.QtWidgets.QMessageBox.critical(self, '错误', str(ret))
        else:
            mission_attribute = ret
            succ, ret = self.area_object.create_fly_mission(mission_attribute)
            if not succ:
                PyQt5.QtWidgets.QMessageBox.critical(self, '错误', str(ret))
            self.close()


class Add_Area_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent, rc):
        PyQt5.QtWidgets.QDialog.__init__(self, parent)
        PyQt5.uic.loadUi('add_area_dialog.ui', self)
        self.rc = rc
        self.reDraw.clicked.connect(self.start_draw)
        self.polygon = None
        self.coors_label.setWordWrap(True)
        self.start_draw()
    
    def start_draw(self):
        self.clear_rubber_band()
        self.rc.gis_canvas.start_draw_polygon(self.draw_finished)
    
    def draw_finished(self, polygon):
        self.polygon = polygon
        self.coors_label.setText(str(self.polygon))
        self.rc.gis_canvas.stop_draw_polygon()
        self.polygon_rubber_band = self.rc.gis_canvas.show_temp_polygon_from_points_list(self.polygon, edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.yellow)
    
    def clear_rubber_band(self):
        if 'polygon_rubber_band' in dir(self):
            self.polygon_rubber_band.hide()
            del(self.polygon_rubber_band)

    def done(self, r):
        self.clear_rubber_band()
        PyQt5.QtWidgets.QDialog.done(self, r)
    
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
                self.close()

class Mission_Widget_Item(PyQt5.QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, rc, type_, binding_object):
        PyQt5.QtWidgets.QTreeWidgetItem.__init__(self, parent)
        self.parent = parent
        self.rc = rc
        self.type = type_
        self.binding_object = binding_object
        self.setText(0, binding_object.name)
        self.set_checked(True)
    
    def get_right_click_menu(self):
        menu = PyQt5.QtWidgets.QMenu(self.rc.main_window)
        if self.type == 'area':
            menu_item = menu.addAction('添加飞行任务')
            menu_item.triggered.connect(self.show_add_fly_mission_dialog)
            menu_item = menu.addAction('删除观测区域')
            menu_item.triggered.connect(lambda: print('TODO 待完成功能：删除观测区域'))
        return menu
    
    def show_add_fly_mission_dialog(self):
        dialog = Add_Fly_Mission_Dialog(self.rc.main_window, self.rc, self.binding_object)
        dialog.show()
    
    def on_click(self):
        self.on_checked_changed()
    
    def set_checked(self, is_checked):
        if is_checked:
            self.setCheckState(0, PyQt5.QtCore.Qt.Checked)
        else:
            self.setCheckState(0, PyQt5.QtCore.Qt.Unchecked)
        self.on_checked_changed()
    
    def on_checked_changed(self):
        if self.checkState(0) == PyQt5.QtCore.Qt.Checked:
            self.binding_object.show()
        else:
            self.binding_object.hide()

class Mission_Widget(PyQt5.QtWidgets.QTreeWidget):
    def __init__(self, main_window, rc):
        PyQt5.QtWidgets.QTreeWidget.__init__(self, main_window)
        self.rc = rc
        self.rc.mission_widget = self
        self.setHeaderLabels(['所有飞行区域'])
        self.itemClicked.connect(self.on_itemclicked)
    
    def on_itemclicked(self, item, column):
        item.on_click()

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if event.buttons() == PyQt5.QtCore.Qt.RightButton:
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
        menu_item.triggered.connect(self.show_add_area_dialog)
        return menu
    
    def show_add_area_dialog(self):
        dialog = Add_Area_Dialog(self.rc.main_window, self.rc)
        dialog.move(self.mapToGlobal(self.pos()))
        dialog.show()
    
    def add_area(self, area_object):
        area_item = Mission_Widget_Item(self, self.rc, 'area', area_object)
        area_item.setExpanded(True)
        return area_item
