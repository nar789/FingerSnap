import ui_plot
import sys
import numpy
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from recorder import *




def plotSomething():
    if SR.newAudio==False: 
        return
    xs,ys=SR.fft()
    c.setData(xs,ys)
    uiplot.qwtPlot.replot()
    SR.newAudio=False
    SR.cnt+=1
    SR.ays=ys+SR.ays
    Y=((ys-SR.before)/SR.before).astype(int)*20+50
    Y.astype(int)
    #print(Y)
    C=numpy.count_nonzero(Y>70)
    
    if C!=0 and SR.detect==True:
        SR.Ccnt+=1
    elif C==0 and SR.detect==True:
        SR.detect=False
        if SR.Ccnt<3:
            print('인식')
        SR.Ccnt=0

    print(C)
    if SR.beforeC==0 and C>150:
        SR.detect=True
    SR.beforeC=C
    if SR.cnt==10:
        SR.cnt=0
        SR.ays=SR.ays/10
        #print(SR.ays)
        SR.before=SR.ays
        SR.ays=numpy.zeros(204)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Ui_win_plot()
    uiplot.setupUi(win_plot)
    uiplot.btnA.clicked.connect(plotSomething)
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    #uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    #uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)
    
    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 1000)
    
    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)
    
    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    SR=SwhRecorder()
    SR.setup()
    SR.continuousStart()

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)