import sys, platform

sys_name = platform.system().lower()
if sys_name.startswith('darwin'):  # mac
    qgispath = '/Applications/QGIS3.app/Contents'
    qgis_pypath = qgispath + '/Resources/python'
    pyqt_plugins = qgispath + '/PlugIns'
    if qgis_pypath not in sys.path:
        sys.path = [qgis_pypath] + sys.path
elif sys_name.startswith('win'):  # windows
    qgispath = 'C:/Program Files/QGIS 3.6'
    pyqt_plugins = qgispath + '/apps/Qt5/plugins'
    qgis_pypath = qgispath + '/apps/qgis/python'
    qgis_python_sitepkgspath = qgispath + '/apps/Python37/Lib/site-packages'
    if qgis_python_sitepkgspath not in sys.path:
        sys.path = [qgis_python_sitepkgspath] + sys.path
    if qgis_pypath not in sys.path:
        sys.path = [qgis_pypath] + sys.path
else:
    raise 'unknown system: %s' % sys_name

import qgis, qgis.core, qgis.gui, PyQt5, PyQt5.uic

if pyqt_plugins not in PyQt5.QtWidgets.QApplication.libraryPaths():
    PyQt5.QtWidgets.QApplication.addLibraryPath(pyqt_plugins)