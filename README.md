# commander

# 代码下载
```
git clone https://github.com/lab505/commander.git
cd commander
git pull --recurse-submodules
```

# 依赖环境及安装方式(windows)
## QGIS
http://qgis.org/downloads/QGIS-OSGeo4W-3.6.0-1-Setup-x86_64.exe (建议安装到默认路径)  
```qt_desinger : C:\Program Files\QGIS 3.6\apps\Qt5\bin\designer.exe```  
## conda with py37
https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Windows-x86_64.exe  
conda install numpy mysql-connector-python pillow

## mysql后端服务
linux/mac: conda install mysql
windows: https://www.mysql.com/cn/downloads/

## GDAL
下载 https://download.lfd.uci.edu/pythonlibs/u2hcgva4/GDAL-2.3.3-cp37-cp37m-win_amd64.whl  
提供者:(https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)  
pip install GDAL-2.3.3-cp37-cp37m-win_amd64.whl


# 程序入口
主窗口&后端服务
```python main_window.py```  
输入数据demo:
```python data_client_demo.py```  

# references
- https://qgis.org/pyqgis/master/
- http://pyqt.sourceforge.net/Docs/PyQt5/class_reference.html
- http://www.resdc.cn/data.aspx?DATAID=200 地图数据下载(省)
- http://mapclub.cn/archives/1814/comment-page-23#comment-3130 地图数据下载(各种)
