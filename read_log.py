import csv
import scipy.io
from scipy.interpolate import interp1d
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
from nk_helpers import colorFader
from plot_setup import plot_setup

'''
Functions and scripts for interpreting Tc measurements with old Python script, where
Rf is read vs universal time and then corresponding ICE temperature is retrived
from log file.

read_ice_log: returns dictionary {time: temperature} from ICE log file
read_mat: returns dictionary {tf: [vals], rf:[vals], norm_rf: [vals]} by comparing 
            Tc meas. MAT file to ICE log dictionary
'''
cg1 = '#d4ad9d'
cg2 = '#4a352f'
# from https://personal.sron.nl/~pault/
YlOrBr = ['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506']

plot_setup()

def get_tc(temps, norm_resistivities):
    r_fxn = interp1d(norm_resistivities, temps)
    return r_fxn(0.5)

DIRECTORY1 = '0628-directwide/'
DIRECTORY2 = '0629-directwide/'
DIRECTORY3 = '0630-directwide/'

def read_ice_log(filename):
    '''
    filename: name of ICE log to read

    returns: dictionary with key: time and value: temperature
    '''
    with open(filename) as csvfile:
        read = csv.reader(csvfile)

        time_to_temp = {}

        for row in read:
            timestamp = int(row[2])
            stage_temp = float(row[4])

            time_to_temp[timestamp] = stage_temp

    return time_to_temp

def read_mat(filename, ice_log, edt=True, superconducting=True, override=False):
    '''
    filename: name of MAT file to read
    edt: boolean indicating need to remove 3600 s from MAT timestamp

    returns: dictionary with at least keys 'rf' corresponding to resistances
    and 'tf' corresponding to temperatures, in order
    '''
    data = scipy.io.loadmat(filename)

    access_data = {}
    
    rfs = [*map(float, data['RF'][0])]
    access_data['rf'] = rfs

    if 'TF' in data and len(data['TF'] > 0) and not override:
        access_data['tf'] = [*map(float, data['TF'][0])]
    elif 'time' in data and len(data['time'] > 0):
        if edt:
            access_data['time'] = [int(time) - 3600 for time in data['time'][0]]
        else:
            access_data['time'] = [*map(int, data['time'][0])]
        
        temps = []
        log_rfs = []
        for i, time in enumerate(access_data['time']):
            if time in ice_log:
                temps.append(ice_log[time])
                log_rfs.append(rfs[i])
            elif time < max(ice_log, key=ice_log.get):
                while time not in ice_log and time < max(ice_log, key=ice_log.get):
                    time += 1
                temps.append(ice_log[time])
                log_rfs.append(rfs[i])
            else:
                pass
                #temps.append(ice_log[max(ice_log, key=ice_log.get)])
        access_data['tf'] = temps
        access_data['log_rf'] = log_rfs
        if superconducting:
            access_data['norm_rf'] =  [(rf - access_data['rf'][-1])/(access_data['rf'][0] - access_data['rf'][-1]) for rf in access_data['rf']]
        else:
            access_data['norm_rf'] = [rf/access_data['rf'][0] for rf in access_data['rf']]

    return access_data

ice_log = read_ice_log(DIRECTORY1+'2022-06-28.log')
#data_1234 = read_mat(DIRECTORY1+'Tc 2022-06-28 15-58-33 sample1234', ice_log, override=True)
data_5678 = read_mat(DIRECTORY1+'Tc 2022-06-28 16-55-21 sample5678.mat', ice_log, override=True)

ice_log29 = read_ice_log(DIRECTORY2+'2022-06-29.log')
data_9101112 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-11-50 sample9101112.mat', ice_log29, override=True)
data_14151617 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-31-34 sample14151617.mat', ice_log29, override=True)
data_21222324 = read_mat(DIRECTORY2+'Tc 2022-06-29 16-46-11 sample21222324.mat', ice_log29, override=True)

ice_log30 = read_ice_log(DIRECTORY3+'2022-06-30.log')
data_1234 = read_mat(DIRECTORY3+'Tc 2022-06-30 14-34-44 sample1234.mat', ice_log30, override=True)

'''
ice_log22 = read_ice_log('Tc_1122/2021-11-22.log')
<<<<<<< HEAD
data_cii = read_mat('Tc_1122/Tc 2021-11-22 12-13-30 11_22_Tc_ITO_EB_1234.mat', ice_log22)
data_di = read_mat('Tc_1122/Tc 2021-11-22 12-20-20 11_22_Tc_ITO_EB_5678.mat', ice_log22)
data_fi = read_mat('Tc_1122/Tc 2021-11-22 12-26-51 11_22_Tc_ITO_EB_9101112.mat', ice_log22)

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
=======
data_1234 = read_mat('Tc_1122/Tc 2021-11-22 12-13-30 11_22_Tc_ITO_EB_1234.mat', ice_log22)
data_5678 = read_mat('Tc_1122/Tc 2021-11-22 12-20-20 11_22_Tc_ITO_EB_5678.mat', ice_log22)
data_9101112 = read_mat('Tc_1122/Tc 2021-11-22 12-26-51 11_22_Tc_ITO_EB_9101112.mat', ice_log22)'''


s=0.1
plt.plot(data_5678['tf'], data_5678['log_rf'], label='100 um', color=YlOrBr[0])
plt.plot(data_14151617['tf'], data_14151617['log_rf'], label='250 um', color=YlOrBr[1])
plt.plot(data_9101112['tf'], data_9101112['log_rf'], label='500 um', color=YlOrBr[2])
plt.plot(data_21222324['tf'], data_21222324['log_rf'], label='1000 um', color=YlOrBr[3])
plt.plot(data_1234['tf'], data_1234['log_rf'], label='2000 um', color=YlOrBr[4])
plt.xlabel('Temperature [K]')
plt.ylabel('Resistivity [Ohm]')
plt.legend()
plt.show()

'''
s=4
plt.scatter(data_none['tf'], data_none['rf'], label='0 C/cm2', s=s, color='black') #label='ITOSA3: 0 C/square', s=s)
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
plt.scatter(data_none['tf'], data_none['norm_rf'], label='0 C/cm2', s=s, color='black') #label='ITOSA3: 0 C/square', s=s)
plt.scatter(data_aii['tf'], data_aii['norm_rf'], label='3.82E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 0/4)) #label='ITOSA3aii: 200 C/square', s=s)
plt.scatter(data_cii['tf'], data_cii['norm_rf'], label='4.26E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 1/4)) # label='ITOSA3cii: 4.26E-2 C/cm2', s=s)
plt.scatter(data_di['tf'], data_di['norm_rf'],label='4.95E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 2/4)) # label='ITOSA3di: ', s=s)
plt.scatter(data_ci['tf'], data_ci['norm_rf'], label='5.94E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 3/4)) #label='ITOSA3ci: 900 C/square', s=s)
plt.scatter(data_fi['tf'], data_fi['norm_rf'], label='9.89E-2 C/cm2', s=s, color=colorFader(cg1, cg2, 4/4)) # label='ITOSA3fi:', s=s)
plt.xlabel('Temperature [K]')
plt.ylabel('Normalized Resistivity')
plt.legend()
plt.show()'''