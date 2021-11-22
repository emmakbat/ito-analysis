import csv
import scipy.io
import matplotlib.pyplot as plt

'''
Functions and scripts for interpreting Tc measurements with old Python script, where
Rf is read vs universal time and then corresponding ICE temperature is retrived
from log file.

read_ice_log: returns dictionary {time: temperature} from ICE log file
read_mat: returns dictionary {tf: [vals], rf:[vals], norm_rf: [vals]} by comparing 
            Tc meas. MAT file to ICE log dictionary
'''

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

def read_mat(filename, ice_log, edt=True, superconducting=True):
    '''
    filename: name of MAT file to read
    edt: boolean indicating need to remove 3600 s from MAT timestamp

    returns: dictionary with at least keys 'rf' corresponding to resistances
    and 'tf' corresponding to temperatures, in order
    '''
    data = scipy.io.loadmat(filename)

    access_data = {}
    
    access_data['rf'] = [*map(float, data['RF'][0])]

    if 'TF' in data and len(data['TF'] > 0):
        access_data['tf'] = [*map(float, data['TF'][0])]
    elif 'time' in data and len(data['time'] > 0):
        if edt:
            access_data['time'] = [int(time) - 3600 for time in data['time'][0]]
        else:
            access_data['time'] = [*map(int, data['time'][0])]
        
        temps = []
        for time in access_data['time']:
            if time in ice_log:
                temps.append(ice_log[time])
            elif time < max(ice_log, key=ice_log.get):
                while time not in ice_log and time < max(ice_log, key=ice_log.get):
                    time += 1
                temps.append(ice_log[time])
            else:
                temps.append(ice_log(max(ice_log, key=ice_log.get)))
        access_data['tf'] = temps
        if superconducting:
            access_data['norm_rf'] =  [(rf - access_data['rf'][-1])/(access_data['rf'][0] - access_data['rf'][-1]) for rf in access_data['rf']]
        else:
            access_data['norm_rf'] = [rf/access_data['rf'][0] for rf in access_data['rf']]

    return access_data

ice_log = read_ice_log('Tc_1114/2021-11-14.log')
data_aii = read_mat('Tc_1114/Tc 2021-11-14 23-27-53 11_14_Tc_ITO_EB_9101112.mat', ice_log)
data_ci = read_mat('Tc_1114/Tc 2021-11-14 23-38-19 11_14_Tc_ITO_EB_13141516.mat', ice_log)
data_none = read_mat('Tc_1114/Tc 2021-11-14 23-58-32 11_14_Tc_ITO_EB_1234.mat', ice_log, superconducting=False)

ice_log22 = read_ice_log('Tc_1122/2021-11-22.log')
data_1234 = read_mat('Tc_1122/Tc 2021-11-22 12-13-30 11_22_Tc_ITO_EB_1234.mat', ice_log22)
data_5678 = read_mat('Tc_1122/Tc 2021-11-22 12-20-20 11_22_Tc_ITO_EB_5678.mat', ice_log22)
data_9101112 = read_mat('Tc_1122/Tc 2021-11-22 12-26-51 11_22_Tc_ITO_EB_9101112.mat', ice_log22)


s=4
plt.scatter(data_aii['tf'], data_aii['rf'], label='200 C/square', s=s) #label='ITOSA3aii: 200 C/square', s=s)
plt.scatter(data_ci['tf'], data_ci['rf'], label='900 C/square', s=s) #label='ITOSA3ci: 900 C/square', s=s)
plt.scatter(data_none['tf'], data_none['rf'], label='0 C/square', s=s) #label='ITOSA3: 0 C/square', s=s)
plt.scatter(data_1234['tf'], data_1234['rf'], label='11/22 1234', s=s)
plt.scatter(data_5678['tf'], data_5678['rf'], label='11/22 5678', s=s)
plt.scatter(data_9101112['tf'], data_9101112['rf'], label='11/22 9101112', s=s)
plt.xlabel('Temperature [K]')
plt.ylabel('4 pt Resistivity')
plt.legend()
plt.show()

s=4
plt.scatter(data_aii['tf'], data_aii['norm_rf'], label='200 C/square', s=s) #label='ITOSA3aii: 200 C/square', s=s)
plt.scatter(data_ci['tf'], data_ci['norm_rf'], label='900 C/square', s=s) #label='ITOSA3ci: 900 C/square', s=s)
plt.scatter(data_none['tf'], data_none['norm_rf'], label='0 C/square', s=s) #label='ITOSA3: 0 C/square', s=s)
plt.scatter(data_1234['tf'], data_1234['norm_rf'], label='11/22 1234', s=s)
plt.scatter(data_5678['tf'], data_5678['norm_rf'], label='11/22 5678', s=s)
plt.scatter(data_9101112['tf'], data_9101112['norm_rf'], label='11/22 9101112', s=s)
plt.xlabel('Temperature [K]')
plt.ylabel('Normalized Resistivity')
plt.legend()
plt.show()