# http://qgis.org/downloads/QGIS-OSGeo4W-3.6.0-1-Setup-x86_64.exe
# https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Windows-x86_64.exe
# https://qgis.org/pyqgis/master/

import logging

qgispath = 'C:/Program Files/QGIS 3.6'
pyqt_plugins = qgispath + '/apps/Qt5/plugins'
qgis_pypath = qgispath + '/apps/qgis/python'
qgis_python_sitepkgspath = qgispath + '/apps/Python37/Lib/site-packages'

def load_qgis():
    try:
        import sys
        sys.path = [qgis_pypath, qgis_python_sitepkgspath] + sys.path
        import PyQt5
        import qgis.core
        import qgis.gui
        return True
    except Exception as e:
        logging.error('load qgis failed')
        logging.exception(e)
        return False
        

def main():
    assert load_qgis()
    import qgis.core
    import qgis.gui
    qgis.core.QgsApplication.addLibraryPath(pyqt_plugins)
    qgis.core.QgsApplication.setPrefixPath(qgispath, True)
    qgs = qgis.core.QgsApplication([], True)
    qgs.initQgis()
    canvas = qgis.gui.QgsMapCanvas()
    canvas.show()

    qgs.exitQgis()

if __name__ == '__main__':
    main()