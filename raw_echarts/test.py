# from raw_echarts.charts import *
# from raw_echarts.miscs import *

# t=Toolbox()
# t(mark={'title':'a'})

import os
import PySide2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

d=os.path.dirname(PySide2.__file__)
d=os.path.join(d,'plugins','platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH']=d

app=QApplication([])
def f(*args):
	print('quting...')
	print(args)

app.aboutToQuit.connect(f)
app.setQuitOnLastWindowClosed(True)

w1=QWidget()
w2=QWidget()
w3=QWidget()

# w2.show()
w3.hide()

w1.close()

print('running...')
print(app.exec_())
print('ended')