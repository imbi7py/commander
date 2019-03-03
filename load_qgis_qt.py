import sys, platform

sys_name = platform.system().lower()
if sys_name.startswith('darwin'):  # mac
    qgispath = '/Applications/QGIS3.app/Contents'
    qgis_pypath = qgispath + '/Resources/python'
    pyqt_plugins = qgispath + '/PlugIns'
    sys.path = [qgis_pypath] + sys.path
elif sys_name.startwith('win'):  # windows
    qgispath = 'C:/Program Files/QGIS 3.6'
    pyqt_plugins = qgispath + '/apps/Qt5/plugins'
    qgis_pypath = qgispath + '/apps/qgis/python'
    qgis_python_sitepkgspath = qgispath + '/apps/Python37/Lib/site-packages'
    sys.path = [qgis_pypath, qgis_python_sitepkgspath] + sys.path
else:
    raise 'unknown system: %s' % sys_name

import qgis, qgis.core, qgis.gui, PyQt5, PyQt5.uic

PyQt5.QtWidgets.QApplication.addLibraryPath(pyqt_plugins)

def get_imported_libs():
    return qgis, PyQt5