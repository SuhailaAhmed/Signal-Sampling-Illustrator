from scipy import interpolate
from scipy.interpolate import interp1d
from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QWidget, QPushButton,QSlider,QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
import numpy as np
import math
import csv
from pyqtgraph.metaarray.MetaArray import axis
from scipy import signal
from scipy.fftpack import fft
import pandas as pd
from pandas import DataFrame

from pyqtgraph.widgets.PlotWidget import PlotWidget

new_sig=[]
dt=0.001
t = np.arange(0, 1, dt)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 689)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_Buttons = QtWidgets.QVBoxLayout()
        self.verticalLayout_Buttons.setObjectName("verticalLayout_buttons")
        self.horizontalLayout_frequencyLabels = QtWidgets.QHBoxLayout()
        self.horizontalLayout_frequencyLabels.setObjectName("horizontalLayout_frequencyLabels")
        self.label_1maxfreq = QtWidgets.QLabel(self.centralwidget)
        self.label_1maxfreq.setObjectName("1maxfreq")
        labels_width = self.label_1maxfreq.width()
        labels_height = self.label_1maxfreq.height()
        self.label_1maxfreq.setFixedSize(labels_width,labels_height)
        self.label_empty1 = QtWidgets.QLabel(self.centralwidget)
        self.label_empty1.setObjectName("empty1")
        self.label_empty1.setFixedSize(210,labels_height)
        self.label_empty2 = QtWidgets.QLabel(self.centralwidget)
        self.label_empty2.setObjectName("empty2")
        self.label_empty2.setFixedSize(self.label_empty2.width(),labels_height)
        self.label_2maxfreq = QtWidgets.QLabel(self.centralwidget)
        self.label_2maxfreq.setObjectName("2maxfreq")
        self.label_2maxfreq.setFixedSize(labels_width,labels_height)
        self.label_3maxfreq = QtWidgets.QLabel(self.centralwidget)
        self.label_empty3 = QtWidgets.QLabel(self.centralwidget)
        self.label_empty3.setObjectName("empty3")
        self.label_empty3.setFixedSize(self.label_empty3.width(),labels_height)
        self.label_3maxfreq.setObjectName("3maxfreq")
        self.label_3maxfreq.setFixedSize(labels_width,labels_height)
        self.horizontalSlider_fsampling = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_fsampling.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_fsampling.setObjectName("horizontalSlfider_fsampling")
        self.gridLayout.addWidget(self.horizontalSlider_fsampling,4,0,1,4)
        # self.horizontalLayout_frequencyLabels.addWidget(self.label_0maxfreq)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_empty1)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_1maxfreq)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_empty2)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_2maxfreq)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_empty3)
        self.horizontalLayout_frequencyLabels.addWidget(self.label_3maxfreq)
        self.gridLayout.addLayout(self.horizontalLayout_frequencyLabels,5,0,1,10)
        self.horizontalSlider_fsampling.setMinimum(0)
        self.horizontalSlider_fsampling.setMaximum(12)
        self.horizontalSlider_fsampling.setValue(0)
        self.horizontalSlider_fsampling.setTickInterval(1)
        self.horizontalSlider_fsampling.setSingleStep(1)
        self.horizontalSlider_fsampling.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider_fsampling.valueChanged.connect(lambda: self.Sampling_change())
        self.pushButton_ShowHide = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ShowHide.setObjectName("pushButton_ShowHide")
        self.gridLayout.addWidget(self.pushButton_ShowHide,4,4)
        self.pushButton_ShowHide.clicked.connect(lambda: self.Show_Hide())
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setGeometry(QtCore.QRect(20, 10, 671, 441))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_mainGraphNew = QtWidgets.QSplitter(self.splitter_2)
        self.splitter_mainGraphNew.setOrientation(QtCore.Qt.Vertical)
        self.splitter_mainGraphNew.setObjectName("splitter_mainGraph")
        self.splitter_2.addWidget(self.splitter_mainGraphNew)
        self.graphicsView_main = PlotWidget(self.splitter_mainGraphNew)
        self.graphicsView_main.setStyleSheet("background: rgb(255,255,255)")
        self.graphicsView_main.setObjectName("graphicsView_main")
        self.graphicsView_main.setTitle("Main Graph")
        self.splitter_mainGraphNew.addWidget(self.graphicsView_main)
        self.graphicsView_reconstruct = PlotWidget(self.splitter_mainGraphNew)
        self.graphicsView_reconstruct.setStyleSheet("background: rgb(255,255,255)")
        self.graphicsView_reconstruct.setObjectName("graphicsView_main")
        self.graphicsView_reconstruct.setTitle("Recovered Signal")
        self.splitter_mainGraphNew.addWidget(self.graphicsView_reconstruct)
        self.splitter_mainGraph = QtWidgets.QSplitter(self.splitter_2)
        self.splitter_mainGraph.setOrientation(QtCore.Qt.Vertical)
        self.splitter_mainGraph.setObjectName("splitter_mainGraph")
        self.graphicsView_composer = PlotWidget(self.splitter_mainGraph)
        self.graphicsView_composer.setStyleSheet("background: rgb(255,255,255)")
        self.graphicsView_composer.setObjectName("graphicsView_composer")
        self.graphicsView_composer.setTitle("Added Signal Preview")
        self.splitter_mainGraph.addWidget(self.graphicsView_composer)
        self.graphicsView_generated_signal = PlotWidget(self.splitter_mainGraph)
        self.graphicsView_generated_signal.setStyleSheet("background: rgb(255,255,255)")
        self.graphicsView_generated_signal.setObjectName("graphicsView_composer")
        self.graphicsView_generated_signal.setTitle("Summation of Signals")
        self.splitter_mainGraph.addWidget(self.graphicsView_generated_signal)
        self.gridLayout.addWidget(self.splitter_2, 0, 0,4,1)
        self.verticalLayout_labels= QtWidgets.QVBoxLayout()
        self.verticalLayout_labels.setObjectName("verticalLayout_labels")
        self.label_freq = QtWidgets.QLabel(self.centralwidget)
        self.label_freq.setObjectName("label_freq")
        self.verticalLayout_labels.addWidget(self.label_freq)
        self.textbox_freq = QtWidgets.QLineEdit(self.centralwidget)
        self.textbox_freq.setObjectName("textEdit_freq")
        self.verticalLayout_labels.addWidget(self.textbox_freq)
        self.textbox_freq.textChanged.connect(self.draw_composer_signal)
        self.label_mag = QtWidgets.QLabel(self.centralwidget)
        self.label_mag.setObjectName("label_mag")
        self.verticalLayout_labels.addWidget(self.label_mag)
        self.textbox_mag = QtWidgets.QLineEdit(self.centralwidget)
        self.textbox_mag.setObjectName("textEdit_mag")
        self.verticalLayout_labels.addWidget(self.textbox_mag)
        self.label_shift = QtWidgets.QLabel(self.centralwidget)
        self.label_shift.setObjectName("label_shift")
        self.verticalLayout_labels.addWidget(self.label_shift)
        self.textbox_phase = QtWidgets.QLineEdit(self.centralwidget)
        self.textbox_phase.setObjectName("textEdit_shift")
        self.verticalLayout_labels.addWidget(self.textbox_phase)
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setObjectName("pushButton_add")
        self.verticalLayout_labels.addWidget(self.pushButton_add)
        self.pushButton_add.clicked.connect(lambda: self.composing_signals())
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.clicked.connect(lambda: self.downladSignal())
        self.verticalLayout_labels.addWidget(self.pushButton_save)
        self.pushButton_move = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_move.setObjectName("pushButton_move")
        self.verticalLayout_labels.addWidget(self.pushButton_move)
        self.pushButton_move.clicked.connect(lambda: self.move_to_main())
        self.pushButton_delete = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.verticalLayout_labels.addWidget(self.pushButton_delete)
        self.pushButton_delete.clicked.connect(lambda: self.delete_signal())
        self.comboBox_signals = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_signals.setObjectName("comboBox_signals")
        self.verticalLayout_labels.addWidget(self.comboBox_signals)
        self.gridLayout.addLayout(self.verticalLayout_labels,0,3,1,2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionopen.triggered.connect(lambda: self.Open_file())
        self.menufile.addAction(self.actionopen)
        self.menubar.addAction(self.menufile.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.toggle_ShowHide = 1
        self.purple_pen = pg.mkPen((255,0,255) , width=1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_ShowHide.setText(_translate("MainWindow", "Show/Hide"))
        self.label_freq.setText(_translate("MainWindow", "Freq. (Hz)"))
        self.label_mag.setText(_translate("MainWindow", "Magnitude"))
        self.label_1maxfreq.setText(_translate("MainWindow", "1 fmax"))
        self.label_2maxfreq.setText(_translate("MainWindow", "2 fmax"))
        self.label_3maxfreq.setText(_translate("MainWindow", "3 fmax"))
        self.label_empty1.setText(_translate("MainWindow", "          "))
        self.label_empty2.setText(_translate("MainWindow", "          "))
        self.label_empty3.setText(_translate("MainWindow", "          "))
        self.label_shift.setText(_translate("MainWindow", "Phase Shift (Deg.)"))
        self.pushButton_add.setText(_translate("MainWindow", "Confirm/Add"))
        self.pushButton_save.setText(_translate("MainWindow", "Save Signal"))
        self.pushButton_move.setText(_translate("MainWindow", "Move To main"))
        self.pushButton_delete.setText(_translate("MainWindow", "Delete"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.actionopen.setText(_translate("MainWindow", "open"))

    def Show_Hide(self):
        self.toggle_ShowHide = self.toggle_ShowHide^1
        
        if self.toggle_ShowHide==1:
            self.graphicsView_reconstruct.show()  
        else:
            self.graphicsView_reconstruct.hide()  

    def draw_composer_signal(self):
        freq=float(self.textbox_freq.text())
        self.graphicsView_composer.clear()
        simple_composed_signal_preview= np.sin(2 * freq * np.pi * t)
        self.graphicsView_composer.plot(t,simple_composed_signal_preview)

    def Get_max_freq(self, Amplitude, time):
        data_amp=[]
        for i in Amplitude:
            if len(data_amp)== len(t):
                break
            else:
                data_amp.append(i)

        n=np.size(time)
        frequencies_array=np.arange(1,np.floor(n/2),dtype ='int')
        data_freq=fft(data_amp)

        freq_mag=(2/n)*abs(data_freq[0:np.size(frequencies_array)])

        imp_freq=freq_mag>0.2
        clean_frequencies_array=imp_freq*frequencies_array
        self.fmax=round(clean_frequencies_array.max())


    def Open_file(self):
        self.graphicsView_composer.clear()
        self.graphicsView_generated_signal.clear()
        self.graphicsView_reconstruct.clear()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open csv', QtCore.QDir.rootPath(), 'csv(*.csv)')
        data_set = pd.read_csv(fileName, header=None)
        self.Save_signal(data_set[0],data_set[1])

    def Save_signal(self,time, Amplitude):
        self.data_amplitude = Amplitude
        self.data_time = time
        self.Get_max_freq(self.data_amplitude, self.data_time)
        self.plot_mainGraph(self.data_amplitude, self.data_time, 0)

    def plot_mainGraph(self, amplitude,time,Fs):
        self.graphicsView_main.plotItem.vb.setLimits(xMin=min(time)-0.01, xMax=max(time),yMin=min(amplitude) - 0.2, yMax=max(amplitude) + 0.2)
        if Fs == 0:
            self.graphicsView_main.clear()
            self.graphicsView_main.plot(time,amplitude)
        else:
            sample_time = 1/Fs
            no_of_samples = math.ceil(max(time))/sample_time
            no_of_samples = math.ceil(no_of_samples)
            index_append= len(time)/no_of_samples
            index_append = math.floor(index_append)
            self.Sample_amp=[]
            self.Sample_time = []
            index = 0
            for i in range(no_of_samples):
                self.Sample_time.append(time[index])
                self.Sample_amp.append(amplitude[index])
                index += index_append

            self.recons_amp = self.sinc_interp(self.Sample_amp,self.Sample_time,time)

            self.graphicsView_main.clear()
            self.graphicsView_reconstruct.clear()
            self.graphicsView_main.plot(time, amplitude)
            self.graphicsView_main.plot(self.Sample_time, self.Sample_amp, symbol='o', pen = None)
            self.graphicsView_main.plot(time, self.recons_amp, pen = self.purple_pen)
            self.graphicsView_reconstruct.plot(time, self.recons_amp, pen=self.purple_pen)
            self.graphicsView_reconstruct.plotItem.vb.setLimits(xMin=min(self.data_time) - 0.01,xMax=max(self.data_time),yMin=min(self.data_amplitude) - 0.2,yMax=max(self.data_amplitude) + 0.2)
    
    def sinc_interp(self, sample_amplitude,sample_time , time):
         if len(sample_amplitude) != len(sample_time):
             raise ValueError('sample time and sample amplitude must be the same length')

         sample_time = np.array(sample_time)
         time = np.array(time)

         # Find the period
         period_time = sample_time[1] - sample_time[0]

         sincM = np.tile(time, (len(sample_time), 1)) - np.tile(sample_time[:, np.newaxis], (1, len(time)))
         recovered_signal = np.dot(sample_amplitude, np.sinc(sincM / period_time))
         return recovered_signal

    def Sampling_change(self):
        value = float(self.horizontalSlider_fsampling.value())
        # if (value/4)*self.fmax*max(self.data_time) <3:
        #     value = 3/(max(self.data_time*self.fmax))
        # else:
        value = value / 4

        self.plot_mainGraph(self.data_amplitude,self.data_time,self.fmax*value)

    def Sampling_change(self):
        value = float(self.horizontalSlider_fsampling.value())
        if (value/4)*self.fmax*max(self.data_time) <3:
            value = 3/(max(self.data_time*self.fmax))
        else:
            value = value / 4

        self.plot_mainGraph(self.data_amplitude,self.data_time,self.fmax*value)

    

    def downladSignal(self):
        to_be_saved = np.c_[t, self.start_graphing]
        np.savetxt("signal.csv", to_be_saved, delimiter=", ")
    
    def composing_signals(self):
        self.pop_up_did_show=0
        try:
            freq = float(self.textbox_freq.text())
            phase_shift = float(self.textbox_phase.text())    
            magnitude = float(self.textbox_mag.text())
            if magnitude <=0:
                self.show_pop_up("The magnitude has to be greater than zero")


        except:
            self.show_pop_up("Kindly make sure that all the values are valid numbers")

        if self.pop_up_did_show==0:
            new_sig.append(magnitude * np.sin(2 * freq * np.pi * t + phase_shift))
            global start_graphing
            self.start_graphing =sum(new_sig)
            self.comboBox_signals.addItem('f={}, phase={}'.format(round(freq),round(phase_shift)))
            self.graphicsView_composer.clear()
            self.graphicsView_generated_signal.clear()
            self.graphicsView_generated_signal.plot(t, self.start_graphing)
    
    def show_pop_up(self,the_message):
        self.pop_up_did_show=1
        msg=QMessageBox()
        msg.setWindowTitle("ERROR")
        msg.setText(the_message)
        show= msg.exec_()

    def delete_signal(self):
        combobox_index = self.comboBox_signals.currentIndex()
        self.comboBox_signals.removeItem(combobox_index)
        new_sig.pop(combobox_index)
        self.start_graphing=sum(new_sig)
        self.graphicsView_generated_signal.clear()
        self.graphicsView_generated_signal.plot(t,self.start_graphing)

    def move_to_main(self):
        self.graphicsView_main.clear()
        self.Save_signal(t,self.start_graphing)
        self.graphicsView_composer.clear()
        self.graphicsView_generated_signal.clear()
        self.comboBox_signals.clear()
        new_sig.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
