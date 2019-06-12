# coding:utf-8
'''
任务控件(Mission Widget相关)

1.先是建立了飞行任务的框Add_Fly_Mission_Dialog，设置了飞行的框里所有值的获取方式，以及当任务发生变化的时候，任务名称、应用范围、载荷以载荷参数的变化，以及平台载荷发生变化后相应的属性值跟着变化
2.框中所有值的获取根据上面设定的获取方式
3.先是定义了创建区域添加框的类Add_Area_Dialog，以及所有值的获取方式，多边形的绘制和坐标的获取（gis_canvas.py）
4.定义了创建飞行区域列表的类函数Mission_Widget_Item，添加列表有添加飞行任务和删除观测区域，添加飞行任务的时候如何与飞行任务的框进行联系，
5.实际任务的添加Mission_Widget，点击右键的添加，有和在右击后弹出区域添加框
6.代码的顺序把实际操作的过程反过来了

'''
import PyQt5, functools
import mission_manager, gis_canvas
from mission_planning import camera, aerocraft, preload_missions, mission_planning
import geo_polygons

class Add_Fly_Mission_Dialog(PyQt5.QtWidgets.QDialog):#添加飞行任务的框
    def __init__(self, parent, rc, area_object):
        PyQt5.QtWidgets.QDialog.__init__(self, parent)
        PyQt5.uic.loadUi('add_fly_mission.ui', self)
        self.rc = rc
        self.area_object = area_object#需要是区域才行
        self.init_data()
        self.camera_attribute_label.setWordWrap(True)#自动换行
        self.aerocraft_attribute_label.setWordWrap(True)#自动换行
        self.preload_missions_listwidget.itemSelectionChanged.connect(
            self.preload_mission_selected_changed)#预设任务里的列表选择项发生变化
        self.camera_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#currentIndex()获取当前comBox的索引，是int类型的值，载荷选择发生变化
        self.aerocraft_cbox.currentIndexChanged.connect(
            self.camera_or_aercraft_selected_changed)#平台选择发生变化
    
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

        
class Add_Area_Dialog(PyQt5.QtWidgets.QDialog):
    def __init__(self, parent, rc):
        PyQt5.QtWidgets.QDialog.__init__(self, parent)
        PyQt5.uic.loadUi('add_area_dialog.ui', self)
        self.rc = rc
        self.reDraw.clicked.connect(self.start_draw)#QPushButton的名字是reDraw
        self.polygon = None
        self.coors_label.setWordWrap(True)#坐标自动换行
        self.start_draw()
        self.pku.clicked.connect(functools.partial(self.use_preload_polygon, 'pku'))
        self.aoxiang.clicked.connect(functools.partial(self.use_preload_polygon, 'aoxiang'))
        self.aoxiang_big.clicked.connect(functools.partial(self.use_preload_polygon, 'aoxiang_big'))
        self.aoxiang_huge.clicked.connect(functools.partial(self.use_preload_polygon, 'aoxiang_huge'))
        self.aoxiang_round.clicked.connect(functools.partial(self.use_preload_polygon, 'aoxiang_round'))
    
    def start_draw(self):
        self.clear_rubber_band()#
        self.rc.gis_canvas.start_draw_polygon(self.draw_finished)
    
    def draw_finished(self, polygon, epsgcode):
        polygon = gis_canvas.trans_points_list(epsgcode, 'EPSG:4326', polygon)
        self.polygon = polygon
        self.coors_label.setText(str(self.polygon))
        self.rc.gis_canvas.stop_draw_polygon()
        self.polygon_rubber_band = self.rc.gis_canvas.show_temp_polygon_from_points_list(
            self.polygon, 'EPSG:4326', edgecolor=PyQt5.QtCore.Qt.black, fillcolor=PyQt5.QtCore.Qt.gray)
    
    def clear_rubber_band(self):
        if 'polygon_rubber_band' in dir(self):
            self.polygon_rubber_band.hide()
            del(self.polygon_rubber_band)

    def use_preload_polygon(self, name_):
        if name_ == 'pku':
            area_polygon = geo_polygons.Polygons.pku['vertex']
        elif name_ == 'aoxiang':
            area_polygon = geo_polygons.Polygons.aoxiang['vertex']
            self.rc.main_window.gis_canvas.zoom_to_polygon(area_polygon, 'EPSG:4326')
        elif name_ == 'aoxiang_big':
            area_polygon = geo_polygons.Polygons.aoxiang_big['vertex']
            self.rc.main_window.gis_canvas.zoom_to_polygon(area_polygon, 'EPSG:4326')
        elif name_ == 'aoxiang_huge':
            area_polygon = geo_polygons.Polygons.aoxiang_huge['vertex']
            self.rc.main_window.gis_canvas.zoom_to_polygon(area_polygon, 'EPSG:4326')
        elif name_ == 'aoxiang_round':
            area_polygon = geo_polygons.Polygons.aoxiang_fly_round['vertex']
            self.rc.main_window.gis_canvas.zoom_to_polygon(area_polygon, 'EPSG:4326')
        else:
            raise '无法识别的多边形 %s' % name_
        self.add_area(area_polygon)

    def done(self, r):
        self.clear_rubber_band()
        self.rc.gis_canvas.stop_draw_polygon()
        PyQt5.QtWidgets.QDialog.done(self, r)
    
    def rejected(self, r):
        self.clear_rubber_band()
        self.rc.gis_canvas.stop_draw_polygon()
        PyQt5.QtWidgets.QDialog.rejected(self, r)
    
    def accept(self):#添加区域的框
        self.rc.gis_canvas.stop_draw_polygon()
        if self.polygon is None:
            PyQt5.QtWidgets.QMessageBox.critical(self, 'ERROR', 'ERROR: please draw a polygon')
        else:
            self.add_area(self.polygon)
    
    def add_area(self, area_polygon):
        area_name = self.area_name_textedit.toPlainText()#获取控件的信息：区域名字
        success, ret = self.rc.mission_manager.add_area(area_name, area_polygon)
        if not success:
            PyQt5.QtWidgets.QMessageBox.critical(self, 'ERROR', 'ERROR: %s' % ret)
        else:
            self.close()

class Mission_Widget_Item(PyQt5.QtWidgets.QTreeWidgetItem):#飞行区域的列表的创建
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
            #menu_item = menu.addAction('添加飞行任务')#向QMeau小控件中添加一个操作按钮，其中包括文字或者涂图标，删除菜单菜单栏额内容用clear（）
            #menu_item.triggered.connect(self.show_add_fly_mission_dialog)
            menu_item = menu.addAction('删除观测区域')
            menu_item.triggered.connect(self.delete)
            menu_item = menu.addAction('转换为字符')
            menu_item.triggered.connect(self.to_text)
            menu_item = menu.addAction('属性')
            menu_item.triggered.connect(self.binding_object.show_attributes)
        elif self.type == 'fly_mission':
            menu_item = menu.addAction('删除飞行任务')
            menu_item.triggered.connect(self.delete)
            menu_item = menu.addAction('转换为字符')
            menu_item.triggered.connect(self.to_text)
            menu_item = menu.addAction('属性')
            menu_item.triggered.connect(self.binding_object.show_attributes)
        return menu
    
    def to_text(self):
        str_ = self.binding_object.to_text()
        dialog = PyQt5.QtWidgets.QMainWindow(self.rc.main_window)
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()
        percentage = 0.8
        dialog.resize(screenRect.width()*percentage, screenRect.height()*percentage)
        dialog.setWindowTitle('转换为字符')
        text_edit = PyQt5.QtWidgets.QPlainTextEdit(dialog)
        dialog.setCentralWidget(text_edit)
        text_edit.setPlainText(str_)
        dialog.show()

    def show_add_fly_mission_dialog(self):#显示添加飞行任务的框，创建框的对象
        dialog = Add_Fly_Mission_Dialog(self.rc.main_window, self.rc, self.binding_object)
        dialog.show()

    def delete(self):
        self.binding_object.delete()
        del self.binding_object
        if self.type == 'area':
            self.parent.takeTopLevelItem(self.parent.indexOfTopLevelItem(self))
        else:
            self.parent.removeChild(self)
        del self

    def on_click(self):#点击后决定是显示还是隐藏
        self.on_checked_changed()
    
    def set_checked(self, is_checked):#判断是否选中了
        if is_checked:
            self.setCheckState(0, PyQt5.QtCore.Qt.Checked)
        else:
            self.setCheckState(0, PyQt5.QtCore.Qt.Unchecked)
        self.on_checked_changed()
    
    def on_checked_changed(self):#如果选中了就显示，没有选中就隐藏
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
        item = self.itemAt(event.pos())#坐标相对于桌面，得到某个位置处单元格的item
        if event.buttons() == PyQt5.QtCore.Qt.RightButton:#右键
            if item:
                menu = item.get_right_click_menu()
                menu.move(event.globalPos())#坐标相对于窗口，在哪右键就在哪出现
                menu.show() 
            else:
                menu = self.get_right_click_menu()
                menu.move(event.globalPos())
                menu.show()
        super(Mission_Widget, self).mousePressEvent(event)
    
    def get_right_click_menu(self):
        menu = PyQt5.QtWidgets.QMenu(self)
        menu_item = menu.addAction('添加飞行区域 - 手动绘制')
        menu_item.triggered.connect(self.show_add_area_dialog)
        menu_item = menu.addAction('添加飞行区域 - 从字符串')
        menu_item.triggered.connect(self.show_add_area_from_text_dialog)
        return menu
    
    def show_add_area_dialog(self):#弹出添加区域的框
        dialog = Add_Area_Dialog(self.rc.main_window, self.rc)
        dialog.move(self.mapToGlobal(self.pos()))
        dialog.move(1120, 580)
        dialog.show()
    
    def show_add_area_from_text_dialog(self):
        dialog = PyQt5.QtWidgets.QMainWindow(self.rc.main_window)
        screenRect = PyQt5.QtWidgets.QApplication.desktop().screenGeometry()
        percentage = 0.5
        dialog.resize(screenRect.width()*percentage, screenRect.height()*percentage)
        dialog.setWindowTitle('从字符串添加飞行区域')

        ok_button = PyQt5.QtWidgets.QPushButton('OK', dialog)
        text_edit = PyQt5.QtWidgets.QTextEdit(dialog)

        ok_func = functools.partial(self.add_area_from_text, dialog, text_edit)
        ok_button.clicked.connect(ok_func)

        layout = PyQt5.QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(text_edit, 1)
        layout.addWidget(ok_button, 2)
        centralwidget = PyQt5.QtWidgets.QWidget(dialog)
        centralwidget.setLayout(layout)
        dialog.setCentralWidget(centralwidget)
        dialog.show()

    def add_area_from_text(self, dialog, text_edit):
        str_ = text_edit.toPlainText()
        print(str_)
        dialog.close()
    
    def add_area(self, area_object):#创建了第一个item
        area_item = Mission_Widget_Item(self, self.rc, 'area', area_object)
        area_item.setExpanded(True)#下一个节点
        return area_item
