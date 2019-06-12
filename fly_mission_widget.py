import PyQt5, PyQt5.QtWidgets
from mission_planning import camera, aerocraft, preload_missions, mission_planning
import mission_widget

class Fly_Mission_Widget(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent, rc):
        self.rc = rc
        self.rc.fly_mission_widget = self
        PyQt5.QtWidgets.QWidget.__init__(self, parent)
        PyQt5.uic.loadUi('fly_mission.ui', self)

        self.init_data()
        self.preload_missions_listwidget.itemSelectionChanged.connect(
            self.preload_mission_selected_changed)#预设任务里的列表选择项发生变化
        self.camera_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#currentIndex()获取当前comBox的索引，是int类型的值，载荷选择发生变化
        self.aerocraft_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#平台选择发生变化
        self.create_area.clicked.connect(self.create_area_func)
        self.generate_mission.clicked.connect(self.accept)
        self.init_areas()
    
    def create_area_func(self):
        dialog = mission_widget.Add_Area_Dialog(self.rc.main_window, self.rc)
        dialog.move(self.pos())
        dialog.show()
    
    def init_areas(self):
        for item in range(self.area_cbox.count()):
            self.area_cbox.removeItem(0)
        for area_name in self.rc.mission_manager.areas.keys():
            self.area_cbox.addItem(area_name)
        for area_name in self.rc.mission_manager.get_preload_board_regions().keys():
            self.available_area_cbox.addItem(area_name)
    
    def preload_mission_selected_changed(self):
        selected_mission_name = self.preload_missions_listwidget.selectedItems()[0].text()#初始化
        mission_attribute = self.preload_missions[selected_mission_name]#任务的字典
        self.mission_name_textedit.setText(selected_mission_name)#
        self.application_textedit.setText(mission_attribute['application'])
        self.camera_cbox.setCurrentText(mission_attribute['cameras'])
        self.aerocraft_cbox.setCurrentText(mission_attribute['aerocraft'])

        self.ground_resolution_m_textedit.setText(str(mission_attribute['ground_resolution_m']))
        self.forward_overlap_textedit.setText(str(mission_attribute['forward_overlap']))
        self.sideway_overlap_textedit.setText(str(mission_attribute['sideway_overlap']))
        self.aerocraft_num.setText(str(mission_attribute['aerocraft_num']))
        self.fly_direction.setText(str(mission_attribute['fly_direction']))

        self.fill_attribute_table(self.mission_attribute, mission_attribute)
    
    def fill_attribute_table(self, attribute_table_widget, attributes_dict):
        attribute_table_widget.clear()
        attribute_table_widget.horizontalHeader().hide()
        attribute_table_widget.setColumnCount(2)
        attribute_table_widget.setRowCount(len(attributes_dict))
        i = 0
        for k in attributes_dict:
            v = str(attributes_dict[k])
            attribute_table_widget.setItem(i, 0, PyQt5.QtWidgets.QTableWidgetItem(k))
            attribute_table_widget.setItem(i, 1, PyQt5.QtWidgets.QTableWidgetItem(v))
            i += 1

    def camera_or_aercraft_selected_changed(self):
        self.selected_camera = self.camera_cbox.currentText()#currentText()获取当前cbox的文本，是QString类型
        self.selected_aerocraft = self.aerocraft_cbox.currentText()
        self.fill_attribute_table(self.aerocraft_attribute, self.preload_aerocrafts[self.selected_aerocraft])
        self.fill_attribute_table(self.camera_attribute, self.preload_cameras[self.selected_camera])
        
    #currentData(int role = Qt::UserRole)获取当前comBox绑定的数据，是QVariant类型。
    def preload_data(self):#几个字典的调用
        self.preload_missions = preload_missions.missions
        self.preload_cameras = camera.cameras
        self.preload_aerocrafts = aerocraft.aerocrafts
    
    def init_data(self):#在预设任务区域和平台载荷的下拉框里添上目前有的任务、平台和载荷
        self.preload_data()
        for mission_name in self.preload_missions:
            self.preload_missions_listwidget.addItem(mission_name)#预设任务区域添加
        for camera_name in self.preload_cameras:
            self.camera_cbox.addItem(camera_name)
        for aerocraft_name in self.preload_aerocrafts:
            self.aerocraft_cbox.addItem(aerocraft_name)#在QComboBox的最后添加一项
        self.preload_missions_listwidget.setCurrentRow(0)
        self.preload_mission_selected_changed()
        self.camera_or_aercraft_selected_changed()
    
    def clear_rubber_band(self):
        if 'polygon_rubber_band' in dir(self):
            self.polygon_rubber_band.hide()
            del(self.polygon_rubber_band)

    def done(self, r):
        PyQt5.QtWidgets.QDialog.done(self, r)
    
    def init_res_attribute(self):
        self.res_attribute = {
            'area_name': '',
            'mission_name': '',
            'application': '',
            'cameras': '',
            'aerocraft': '',
            'fly_direction': '',
            'ground_resolution_m': '',
            'sideway_overlap': '',
            'forward_overlap': '',
            'aerocraft_num': '',
            'board_region_name': '',
        }
    
    #def res_attribute_changed(self):

    #def set_res_attribute(self):
    
    def accept(self):
        params = {
            'area_name': self.area_cbox.currentText(),
            'mission_name': self.mission_name_textedit.toPlainText(),
            'application': self.application_textedit.toPlainText(),
            'cameras': self.camera_cbox.currentText(),
            'aerocraft': self.aerocraft_cbox.currentText(),
            'fly_direction': self.fly_direction.toPlainText(),
            'ground_resolution_m': self.ground_resolution_m_textedit.toPlainText(),
            'sideway_overlap': self.sideway_overlap_textedit.toPlainText(),
            'forward_overlap': self.forward_overlap_textedit.toPlainText(),
            'aerocraft_num': self.aerocraft_num.toPlainText(),
            'board_region_name': self.available_area_cbox.currentText(),
        }
        succ, ret = self.rc.mission_manager.add_fly_mission_to_area(params)
        if not succ:
            PyQt5.QtWidgets.QMessageBox.critical(self, '错误', str(ret))