from xml import dom
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
from nk_helpers import colorFader
from plot_setup import plot_setup
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

plot_setup(fig_x=7.2, fig_y=4.6)

DIRECTORY1 = '0628-directwide/'
DIRECTORY2 = '0629-directwide/'
DIRECTORY3 = '0630-directwide/'

ice_log = read_ice_log(DIRECTORY1+'2022-06-28.log')
#data_1234 = read_mat(DIRECTORY1+'Tc 2022-06-28 15-58-33 sample1234', ice_log, override=True)
data_5678 = read_mat(DIRECTORY1+'Tc 2022-06-28 16-55-21 sample5678.mat', ice_log, override=True)

ice_log29 = read_ice_log(DIRECTORY2+'2022-06-29.log')
data_9101112 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-11-50 sample9101112.mat', ice_log29, override=True)
data_14151617 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-31-34 sample14151617.mat', ice_log29, override=True)
data_21222324 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-46-11 sample21222324.mat', ice_log29, override=True)

ice_log30 = read_ice_log(DIRECTORY3+'2022-06-30.log')
data_1234 = read_mat(DIRECTORY3+'Tc 2022-06-30 14-34-44 sample1234.mat', ice_log30, override=True)

DOME_DIRECTORY = 'data/Tc_data/Tc_1122/'
DOME_DIRECTORY2 = 'data/Tc_data/Tc_1114/'
ice_log14 = read_ice_log(DOME_DIRECTORY2+'2021-11-14.log')
data_aii = read_mat(DOME_DIRECTORY2+'Tc 2021-11-14 23-27-53 11_14_Tc_ITO_EB_9101112.mat', ice_log14)
data_ci = read_mat(DOME_DIRECTORY2+'Tc 2021-11-14 23-38-19 11_14_Tc_ITO_EB_13141516.mat', ice_log14)

ice_log22 = read_ice_log(DOME_DIRECTORY+'2021-11-22.log')
data_cii = read_mat(DOME_DIRECTORY+'Tc 2021-11-22 12-13-30 11_22_Tc_ITO_EB_1234.mat', ice_log22)
data_di = read_mat(DOME_DIRECTORY+'Tc 2021-11-22 12-20-20 11_22_Tc_ITO_EB_5678.mat', ice_log22)
data_fi = read_mat(DOME_DIRECTORY+'Tc 2021-11-22 12-26-51 11_22_Tc_ITO_EB_9101112.mat', ice_log22)

all_sc_data = [data_aii, data_cii, data_di, data_ci, data_fi]
reduction = [3.82E-2, 4.26E-2, 4.95E-2, 5.94E-2, 9.89E-2]
tcs = []
for data in all_sc_data:
    tc = get_tc(data['tf'], data['norm_rf'])
    print(tc)
    tcs.append(tc)

dome = Polynomial.fit(reduction, tcs, 2)

plt.plot(*dome.linspace(), '--', color='gray')
plt.scatter(reduction, tcs, color='black')
plt.xlabel('Reduction amount [C/cm2]')
plt.ylabel('Transition temperature [K]')

plt.savefig('tc_dome.svg')

data_1234 = read_mat('data/Tc_data/Tc_1122/Tc 2021-11-22 12-13-30 11_22_Tc_ITO_EB_1234.mat', ice_log22)
data_5678 = read_mat('data/Tc_data/Tc_1122/Tc 2021-11-22 12-20-20 11_22_Tc_ITO_EB_5678.mat', ice_log22)
data_9101112 = read_mat('data/Tc_data/Tc_1122/Tc 2021-11-22 12-26-51 11_22_Tc_ITO_EB_9101112.mat', ice_log22)

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

#plt.plot(data_5678['tf'], offset_resistivity(data_5678, 350), label='100 um', color=YlOrBr[0])
#plt.plot(data_14151617['tf'], offset_resistivity(data_14151617), label='250 um', color=YlOrBr[1])
#plt.plot(data_9101112['tf'][50:], offset_resistivity(data_9101112)[50:], label='500 um', color=YlOrBr[2])
#plt.plot(data_21222324['tf'], offset_resistivity(data_21222324), label='1000 um', color=YlOrBr[3])
#plt.plot(data_1234['tf'], offset_resistivity(data_1234), label='2000 um', color=YlOrBr[4])
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
'''
s=4
#plt.scatter(data_none['tf'], data_none['rf'], label='0 C/cm2', s=s, color='black') #label='ITOSA3: 0 C/square', s=s)
plt.scatter(data_aii['tf'], data_aii['rf'], label='3.82E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 0)) #label='ITOSA3aii: 200 C/square', s=s)
plt.scatter(data_cii['tf'], data_cii['rf'], label='4.26E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 1/4)) # label='ITOSA3cii: 4.26E-2 C/cm2', s=s)
plt.scatter(data_di['tf'], data_di['rf'],label='4.95E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 2/4)) # label='ITOSA3di: ', s=s)
plt.scatter(data_ci['tf'], data_ci['rf'], label='5.94E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 3/4)) #label='ITOSA3ci: 900 C/square', s=s)
plt.scatter(data_fi['tf'], data_fi['rf'], label='9.89E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 4/4)) # label='ITOSA3fi:', s=s)
plt.xlabel('Temperature [K]')
plt.ylabel('4 pt Resistivity')
plt.legend()
plt.show()

s=4
#plt.scatter(data_none['tf'], data_none['norm_rf'], label='0 C/cm2', s=s, color='black') #label='ITOSA3: 0 C/square', s=s)
plt.scatter(data_aii['tf'], data_aii['norm_rf'], label='3.82E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 0/4)) #label='ITOSA3aii: 200 C/square', s=s)
plt.scatter(data_cii['tf'], data_cii['norm_rf'], label='4.26E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 1/4)) # label='ITOSA3cii: 4.26E-2 C/cm2', s=s)
plt.scatter(data_di['tf'], data_di['norm_rf'],label='4.95E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 2/4)) # label='ITOSA3di: ', s=s)
plt.scatter(data_ci['tf'], data_ci['norm_rf'], label='5.94E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 3/4)) #label='ITOSA3ci: 900 C/square', s=s)
plt.scatter(data_fi['tf'], data_fi['norm_rf'], label='9.89E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 4/4)) # label='ITOSA3fi:', s=s)
plt.xlabel('Temperature [K]')
plt.ylabel('Normalized Resistivity')
plt.legend()
plt.show()'''