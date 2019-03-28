# coding:utf-8
import load_libs
import sys, qgis, qgis.core, qgis.gui, PyQt5
import gis_canvas
import mission_planning.route_planning


class MyWnd_fortest(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        PyQt5.QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 1000)
        self.canvas = gis_canvas.Gis_Canvas(self)
        self.canvas.resize(1000, 800)
        self.canvas.move(0, 0)
        self.button = PyQt5.QtWidgets.QPushButton(self)
        self.button.move(0, 800)
        self.button.clicked.connect(self.onClick)
        self.canvas.zoom_to_pku()

        shoot_coors_geo, photo_ground_rectangles_geo, debug_info = mission_planning.route_planning.plan_a_route_for_test()
        shooting_area = debug_info['shooting_area']
        self.canvas.show_temp_polyline_from_points_list(shoot_coors_geo, '4326',
                                                       color=PyQt5.QtCore.Qt.blue,
                                                       width=1,
                                                       line_style=PyQt5.QtCore.Qt.SolidLine)
        self.canvas.show_temp_polyline_from_points_list(shooting_area+shooting_area[:1], '4326',
                                                       color=PyQt5.QtCore.Qt.black,
                                                       width=1,
                                                       line_style=PyQt5.QtCore.Qt.DashDotDotLine)
        for rec in photo_ground_rectangles_geo:
            self.canvas.show_temp_polyline_from_points_list(rec+rec[:1], '4326',
                                                           color=PyQt5.QtCore.Qt.red,
                                                           width=1,
                                                           line_style=PyQt5.QtCore.Qt.SolidLine)

    def onClick(self):
        print('ok')
        self.canvas.zoom_to_china()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    form = MyWnd_fortest()
    form.show()
    sys.exit(app.exec_())
