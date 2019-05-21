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
        self.camera_attribute_label.setWordWrap(True)#自动换行
        self.aerocraft_attribute_label.setWordWrap(True)#自动换行
        self.preload_missions_listwidget.itemSelectionChanged.connect(
            self.preload_mission_selected_changed)#预设任务里的列表选择项发生变化
        self.camera_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#currentIndex()获取当前comBox的索引，是int类型的值，载荷选择发生变化
        self.aerocraft_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#平台选择发生变化
        self.create_area.clicked.connect(self.create_area_func)
        self.init_areas()
    
    def create_area_func(self):
        dialog = mission_widget.Add_Area_Dialog(self.rc.main_window, self.rc)
        dialog.show()
    
    def init_areas(self):
        for item in range(self.area_cbox.count()):
            self.area_cbox.removeItem(0)
        for area_name in self.rc.mission_manager.areas.keys():
            self.area_cbox.addItem(area_name)
    
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
    
    def camera_or_aercraft_selected_changed(self):
        self.selected_camera = self.camera_cbox.currentText()#currentText()获取当前cbox的文本，是QString类型
        self.camera_attribute_label.setText(str(self.preload_cameras[self.selected_camera]))#平台发生变化，平台参数也会发生变化
        self.selected_aerocraft = self.aerocraft_cbox.currentText()
        self.aerocraft_attribute_label.setText(str(self.preload_aerocrafts[self.selected_aerocraft]))#载荷发生变化，参数label也发生变化
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
    
    def accept(self):
        self.params = {
            'area': self.area_object.polygon,
            'mission_name': self.mission_name_textedit.toPlainText(),
            'application': self.application_textedit.toPlainText(),
            'cameras': self.camera_cbox.currentText(),
            'aerocraft': self.aerocraft_cbox.currentText(),
            'fly_direction': self.fly_direction.toPlainText(),
            'ground_resolution_m': self.ground_resolution_m_textedit.toPlainText(),
            'sideway_overlap': self.sideway_overlap_textedit.toPlainText(),
            'forward_overlap': self.forward_overlap_textedit.toPlainText(),
            'aerocraft_num': self.aerocraft_num.toPlainText(),
        }
        succ, ret = mission_planning.mission_planning(
            area_points_list=self.params['area'],
            mission_name=self.params['mission_name'],
            aerocraft=self.params['aerocraft'],
            camera=self.params['cameras'],
            ground_resolution_m=self.params['ground_resolution_m'],
            forward_overlap=self.params['forward_overlap'],
            sideway_overlap=self.params['sideway_overlap'],
            fly_direction=self.params['fly_direction'],
            application=self.params['application'],
            aerocraft_num=self.params['aerocraft_num'],
            )
        if not succ:
            PyQt5.QtWidgets.QMessageBox.critical(self, '错误', str(ret))
        else:
            mission_attribute = ret
            succ, ret = self.area_object.create_fly_mission(mission_attribute)
            if not succ:
                PyQt5.QtWidgets.QMessageBox.critical(self, '错误', str(ret))
            self.close()