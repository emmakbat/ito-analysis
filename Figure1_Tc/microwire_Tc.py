from xml import dom
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import make_interp_spline
from tc_icelog_helpers import *
from scipy.io import savemat

'''
Scripts for interpreting Tc measurements taken on the ICE, where the temperature log
and resistance measurements happen on two different computers, so they have to be
matched back up later on. See tc_icelog_helpers for more
'''
cg1 = '#d4ad9d'
cg2 = '#4a352f'
# from https://personal.sron.nl/~pault/
YlOrBr = ['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506']

def plot_setup(fig_x=7.2, fig_y=4.6, dpi=80, SMALL_SIZE=12, MEDIUM_SIZE=14, BIGGER_SIZE=16, bottom_buffer=0.3, left_buffer=0.15):
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('figure', figsize=(fig_x, fig_y))
    plt.rc('figure', dpi=dpi)
    return

plot_setup(fig_x=7.2, fig_y=4.6)

DIRECTORY1 = 'Tc/0628-directwide/'
DIRECTORY2 = 'Tc/0629-directwide/'
DIRECTORY3 = 'Tc/0630-directwide/'

ice_log = read_ice_log(DIRECTORY1+'2022-06-28.log')
#data_1234 = read_mat(DIRECTORY1+'Tc 2022-06-28 15-58-33 sample1234', ice_log, override=True)
data_5678 = read_mat(DIRECTORY1+'Tc 2022-06-28 16-55-21 sample5678.mat', ice_log, override=True)

ice_log29 = read_ice_log(DIRECTORY2+'2022-06-29.log')
data_9101112 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-11-50 sample9101112.mat', ice_log29, override=True)
data_14151617 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-31-34 sample14151617.mat', ice_log29, override=True)
data_21222324 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-46-11 sample21222324.mat', ice_log29, override=True)

ice_log30 = read_ice_log(DIRECTORY3+'2022-06-30.log')
data_1234 = read_mat(DIRECTORY3+'Tc 2022-06-30 14-34-44 sample1234.mat', ice_log30, override=True)


inflection_point = np.argmax(data_9101112['tf'])
offset_r = offset_resistivity(data_9101112)
t1 = np.array(data_9101112['tf'][50:inflection_point])
r1 = np.array(offset_r[50:inflection_point])
t2 = np.array(data_9101112['tf'][inflection_point:])
r2 = np.array(offset_r[inflection_point:])

r1 = r1[np.argsort(t1)]
t1 = t1[np.argsort(t1)]
r2 = r2[np.argsort(t2)]
t2 = t2[np.argsort(t2)]

s=3
plt.figure()
plt.gcf().subplots_adjust(bottom=0.2)
plt.scatter(t2, r2, color=YlOrBr[2], s=s)
#plt.plot(t2, savgol_filter(savgol_filter(r2, 31, 0), 31, 0), color='black')
plt.scatter(t1, r1, color=YlOrBr[2], s=s)
#plt.plot(t1, savgol_filter(r1, 11, 0), color='black')
#plt.plot(t1, savgol_filter(savgol_filter(r1, 11, 0), 11, 0), color='black')

plt.plot(data_5678['tf'], offset_resistivity(data_5678, 350), label='100 um', color=YlOrBr[0])
plt.plot(data_14151617['tf'], offset_resistivity(data_14151617), label='250 um', color=YlOrBr[1])
plt.plot(data_9101112['tf'][50:], offset_resistivity(data_9101112)[50:], label='500 um', color=YlOrBr[2])
plt.plot(data_21222324['tf'], offset_resistivity(data_21222324), label='1000 um', color=YlOrBr[3])
plt.plot(data_1234['tf'], offset_resistivity(data_1234), label='2000 um', color=YlOrBr[4])
plt.xlabel('Temperature [K]')
plt.ylabel('Resistivity [Ohm]')
plt.legend()
#plt.savefig('tc_2000um.svg')
plt.show()

data = {
    't_2000u': data_1234['tf'],
    'r_2000u': data_1234['rf'],
    'offr_2000u': offset_resistivity(data_1234),
    't_100u': data_5678['tf'],
    'r_100u': data_5678['rf'],
    'offr_100u': offset_resistivity(data_5678),
    't_500u': data_9101112['tf'],
    'r_500u': data_9101112['rf'],
    'offr_500u': offset_r,
    't_250u': data_14151617['tf'],
    'r_250u': data_14151617['rf'],
    'offr_250u': offset_resistivity(data_14151617),
    't_1000u': data_21222324['tf'],
    'r_1000u': data_21222324['rf'],
    'offr_1000u': offset_resistivity(data_21222324)
}

savemat('widewire_tc.mat', data)