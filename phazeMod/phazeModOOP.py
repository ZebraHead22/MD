import ui
import sys
import random
import numpy as np
import scipy as sp
from scipy import fftpack
from PyQt6 import QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from numpy.fft import fft, ifft
from scipy.fft import rfft, rfftfreq

class MainApplication(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    "Equation parameters"
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Setup default values for freq1 = 100 THz, coeff1 = 1, sum = 1
        self.freq_dsb.setValue(100)  # freq1 = 100 THz
        self.c1_dsb.setValue(1)  # coeff1 = 1
        self.sum_dsb.setValue(1)  # sum = 1

        # Setup SpinBoxes
        self.setup_spin_box(self.c1_dsb, self.label_2, self.horizontalLayout_3)
        self.setup_spin_box(self.c2_dsb, self.label_3, self.horizontalLayout_2)
        self.setup_spin_box(self.c3_dsb, self.label_6, self.horizontalLayout_7)
        self.setup_spin_box(self.freq_dsb, self.label, self.horizontalLayout_5)
        self.setup_spin_box(self.freq2_dsb, self.label_5, self.horizontalLayout_6)
        self.setup_spin_box(self.freq3_dsb, self.label_4, self.horizontalLayout_4)
        self.setup_spin_box(self.sum_dsb, self.label_7, self.horizontalLayout_8)

        # Automatically plot when the window is loaded
        self.plot()

    def setup_spin_box(self, spin_box, label, layout):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel(label))
        spin_box.valueChanged.connect(self.plot)  # Connect value change to plotting function
        hbox.addWidget(spin_box)
        layout.addLayout(hbox)

    def plot(self):  # Compute and plot graphics
        # Read parameters
        self.c1 = self.c1_dsb.value()
        self.c2 = self.c2_dsb.value()
        self.c3 = self.c3_dsb.value()
        self.sum = self.sum_dsb.value()
        self.freq = self.freq_dsb.value() * (10 ** 12)
        self.freq2 = self.freq2_dsb.value() * (10 ** 12)
        self.freq3 = self.freq3_dsb.value() * (10 ** 12)
        
        # Compute signal
        self.SR = 10 ** 18  # No. of samples per second
        Ts = 1. / self.SR  # Sampling interval
        self.t = np.arange(0, 0.5 * 10 ** (-12), Ts)
        
        o = self.c3 * np.sin(2 * np.pi * self.freq3 * self.t)  # Fluctuation function
        signal_main = self.c1 * np.sin(2 * np.pi * self.freq * self.t + o)
        signal_additional = self.c2 * np.cos(2 * np.pi * self.freq2 * self.t + o)

        if self.sum == 1:
            self.s = signal_main - signal_additional
        elif self.sum >= 2:
            variables_names = {}
            for i in range(2, int(self.sum) + 1):
                key = 'member_' + str(i)
                o = (random.random() * self.c3) * \
                    np.sin(2 * np.pi * (random.random() * self.freq3) * self.t)
                value = ((random.random() * self.c1) * np.sin(2 * np.pi * (random.random() * self.freq) * self.t + o)) - \
                        ((random.random() * self.c2) * np.cos(2 * np.pi * (random.random() * self.freq2) * self.t + o))
                variables_names[key] = value

            names_list = list(variables_names.values())
            summarize = sum(names_list)
            additional_signals = np.array(summarize)
            self.s = (signal_main - signal_additional) + additional_signals

        else:
            raise TypeError("Неверные данные")

        self.X = fft(self.s)
        N = len(self.X)
        n = np.arange(N)
        T = N / self.SR
        self.freq = n / T
        
        # Clear windows before plotting
        self.time_wid.clear()
        self.spec_wid.clear()
        
        # Plot ATR
        self.time_wid.setLabel('bottom', 'time', units='s')
        self.time_wid.setLabel('left', 'Amplitude', units='a.u.')
        self.time_wid.plot(self.t, self.s, pen='r')
        
        # Plot spectre
        self.spec_wid.setLabel('bottom', 'k', units='Hz')
        self.spec_wid.setLabel('left', 'Amplitude', units='a.u.')
        self.spec_wid.setXRange(0, 10 ** 15, padding=0)
        self.spec_wid.plot(self.freq, np.abs(self.X), pen='r')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
