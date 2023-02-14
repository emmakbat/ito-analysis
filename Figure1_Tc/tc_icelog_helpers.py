import csv
import scipy.io
import numpy as np
from scipy.interpolate import interp1d

'''
read_ice_log: returns dictionary {time: temperature} from ICE log file
read_mat: returns dictionary {tf: [vals], rf:[vals], norm_rf: [vals]} by comparing 
            Tc meas. MAT file to ICE log dictionary
'''

def get_tc(temps, resistivities, norm=True, highT_r=None):
    if not norm:
        norm_resistivities = []
        for resistivitiy in resistivities:
            norm_resistivities.append(resistivitiy/highT_r)
    else:
        norm_resistivities = resistivities
    r_fxn = interp1d(norm_resistivities, temps)
    return r_fxn(0.1)

def offset_resistivity(data, num_low=100, num_start=0):
    lowtemp_r = np.sum(data['log_rf'][num_start:(num_low+num_start)])/num_low 
    offset_r = []
    for i, r in enumerate(data['log_rf']):
        offset_r.append(r-lowtemp_r)
    return offset_r

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