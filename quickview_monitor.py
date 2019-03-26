import PyQt5
import img_utils

class Filter_Combobox(PyQt5.QtWidgets.QComboBox):
    def __init__(self, rc, parent, filter_name, quickview_monitor):
        self.rc = rc
        PyQt5.QtWidgets.QComboBox.__init__(self, parent)
        self.quickview_monitor = quickview_monitor
        self.filter_name = filter_name
        self.activated[str].connect(self.on_selected_changed)
        self.init_items()

    def init_items(self):
        self.items = ['All', 'None']
        self.items = self.items + self.rc.cfg.get(
            'quickview_filter_item_preload', {}).get(
                self.filter_name, [])
        for item in self.items:
            self.addItem(item)
        self.setCurrentIndex(self.findText('All'))
        self.on_selected_changed('All')

    def on_selected_changed(self, selected_item):
        self.selected_item = selected_item
        self.quickview_monitor.clear_img()

    def passed_filter(self, value):
        if len(value) > 0 and value not in self.items:
            self.items.append(value)
            self.addItem(value)

        if self.selected_item == 'All':
            return True
        elif self.selected_item == 'None':
            return False
        else:
            if value == self.selected_item:
                return True
            else:
                return False


class Quickview_Monitor(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent, rc, name):
        self.rc = rc
        self.name = name
        PyQt5.QtWidgets.QWidget.__init__(self, parent)

        self.imglabel = PyQt5.QtWidgets.QLabel(self)
        self.init_filter_comboboxes()
        self.init_layout()

    def clear_img(self):
        self.imglabel.clear()

    def init_layout(self):
        vertical_layout = PyQt5.QtWidgets.QVBoxLayout()
        self.setLayout(vertical_layout)
        horizontal_layout = PyQt5.QtWidgets.QHBoxLayout()
        for filter_name, combobox in self.filter_comboboxes.items():
            namelabel = PyQt5.QtWidgets.QLabel(self)
            namelabel.setText(filter_name+':')
            horizontal_layout.addWidget(namelabel)
            horizontal_layout.addWidget(combobox)
        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.imglabel)

    def init_filter_comboboxes(self):
        self.filter_comboboxes = {}

        def init_comboboxe(filter_name):
            one_filter = Filter_Combobox(self.rc, self, filter_name, self)
            self.filter_comboboxes[filter_name] = one_filter

        init_comboboxe('aircraft_type')
        init_comboboxe('sensor_type')

    def passed_filters(self, one_quickview_data):
        if self.filter_comboboxes['aircraft_type'].passed_filter(one_quickview_data['aircraft_type']):
            if self.filter_comboboxes['sensor_type'].passed_filter(one_quickview_data['sensor_type']):
                return True
        return False

    def check_and_show_quickview(self, one_quickview_data):
        if self.passed_filters(one_quickview_data):
            if 'pil_img' not in one_quickview_data:
                one_quickview_data['pil_img'] = img_utils.str_to_img(one_quickview_data['data'])
            self.show_img(one_quickview_data['pil_img'])
            self.show_infor(one_quickview_data)

    def show_img(self, pil_img):
        labelsize = self.imglabel.size()
        pil_img = pil_img.resize((labelsize.width(), labelsize.height()))
        tmp_file_name = '.quickview_monitor_tmp.%s.png' % self.name
        pil_img.save(tmp_file_name, 'png')
        self.imglabel.setPixmap(PyQt5.QtGui.QPixmap(tmp_file_name))

    def show_infor(self,one_quickview_data):
        img_infor='平台：'
        img_infor=img_infor+one_quickview_data['aircraft_type']+'\n'+'传感器：'+one_quickview_data['sensor_type']
        self.imglabel.setToolTip(img_infor)
           
        
    


