import os
import re
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

folder = r'/Users/max/Yandex.Disk.localized/NamdData/3part_calculation/ff/lowTemp/500ps/'

first = pd.read_csv(
    folder + r'ff_1.dat', delimiter=' ', index_col=None)
first.rename(columns={'#': 'frame', 'Unnamed: 2': 'dip_x', 'Unnamed: 4': 'dip_y',
                   'Unnamed: 6': 'dip_z', 'Unnamed: 8': '|dip|'}, inplace=True)

second = pd.read_csv(
    folder + r'ff_2.dat', delimiter=' ', index_col=None)
second.rename(columns={'#': 'frame', 'Unnamed: 2': 'dip_x', 'Unnamed: 4': 'dip_y',
                   'Unnamed: 6': 'dip_z', 'Unnamed: 8': '|dip|'}, inplace=True)

third = pd.read_csv(
   folder + r'ff_3.dat', delimiter=' ', index_col=None)
third.rename(columns={'#': 'frame', 'Unnamed: 2': 'dip_x', 'Unnamed: 4': 'dip_y',
                   'Unnamed: 6': 'dip_z', 'Unnamed: 8': '|dip|'}, inplace=True)

frames = [first, second, third]
df = pd.concat(frames)
df.dropna(how='all', axis=1, inplace=True)
time = [x*0.005 for x in range(0, 300000)]
df.insert(1, "Time", (time))

y_samples = np.array(df['dip_x'])
x_samples = np.array(df["Time"])

fieldtime = 500
ylimit = 35

plt.gcf().clear()
plt.plot(x_samples, y_samples, c='black', linewidth=1)
plt.vlines(fieldtime, -1*int(ylimit), ylimit, color='r')
plt.vlines(int(max(x_samples)-fieldtime), -1*int(ylimit), ylimit, color='r')
plt.ylabel('Dipole moment (D)')
plt.xlabel('Time (ps)')
plt.ylim(-1*int(ylimit), ylimit)
plt.grid()
plt.savefig(folder+'/'+'ff_x.png')
