import matplotlib.pyplot as plt 
import csv
import numpy as np

class ItoData:
    def __init__(self, id, apparatus, status, Rs, thickness, current='None', 
    time='None', postRs='None', postThickness='None', postSR='None', Tc='None', Rlong='None'):
        self.id = id 
        self.apparatus = apparatus
        self.status = status
        self.current = current
        self.time = time 
        self.Rs = Rs 
        self.thickness = thickness
        self.postRs = postRs
        self.postThickness = postThickness
        self.postSR = postSR
        self.Tc = Tc
        self.Rlong = Rlong

        if id[2] == '0':
            self.wafer = 'old'
        elif id[2] == '1':
            self.wafer = 'new'

def read_csv(filename):
    with open(filename) as csvfile:
        read = csv.reader(csvfile)
        next(read)

        samples = []
        sample_dict = {}

        for row in read:
            id = row[0]
            apparatus = row[1]

            if len(row[7]) > 0:
                Rs = float(row[7])
            else:
                Rs = 'None'

            # prioritize thickness measured on VASE if present
            if len(row[10]) > 0:
                if len(row[11]) > 0:
                    thickness = float(row[10]) + float(row[11])
                else:
                    thickness = float(row[10])
            elif len(row[8]) > 0:
                thickness = float(row[8])
            else:
                thickness = 'None'

            # if process worked, look at post intercalation
            status = False
            postRs = 'None'
            postThickness = 'None'
            postSR = 'None'
            Rlong = 'None'

            if row[4] == 'yes':
                status = True
                if len(row[12]) > 0:
                    Rlong = float(row[12])

                if len(row[14]) > 0:
                    postRs = float(row[14])

                if len(row[16]) > 0:
                    postThickness = float(row[16])
                    postSR = float(row[17])

            if apparatus != 'upstairs/DAQ':
                current = 'None'
                time = 'None'
            else:
                current = row[2]
                time = row[3]

            if len(row[19]) > 0:
                Tc = float(row[19])
            else:
                Tc = 'None'

            samples.append(ItoData(id, apparatus, status, Rs, thickness, current,
                time, postRs, postThickness, postSR, Tc, Rlong))
            sample_dict[id] = ItoData(id, apparatus, status, Rs, thickness, current,
                time, postRs, postThickness, postSR, Tc, Rlong)
    return samples, sample_dict

samples, sample_dict = read_csv('ITO_summary.csv')

old_samples = [ito for ito in samples if ito.wafer == 'old']
new_samples = [ito for ito in samples if ito.wafer == 'new']

'''
initial_Rs = [ito.Rs for ito in samples if ito.Rs != 'None']
biggest = max(initial_Rs)
smallest = min(initial_Rs)
width = (biggest - smallest)/(len(initial_Rs))

old_initRs = [ito.Rs for ito in old_samples if ito.Rs != 'None']
new_initRs = [ito.Rs for ito in new_samples if ito.Rs != 'None']

bins = np.arange(smallest, biggest, width)

plt.hist([old_initRs, new_initRs], bins)
plt.xlabel('Initial Sheet Resistance')
plt.ylabel('Number of Samples')
plt.title('Histogram of Sample Sheet Resistance')
plt.show()'''

'''
old_x = []
old_y = []
for sample in old_samples:
    thickness = sample.thickness
    Rs = sample.Rs

    if thickness != 'None' and Rs != 'None':
        old_x.append(thickness)
        old_y.append(Rs)

new_x = []
new_y = []
for sample in new_samples:
    thickness = sample.thickness
    Rs = sample.Rs

    if thickness != 'None' and Rs != 'None':
        new_x.append(thickness)
        new_y.append(Rs)

plt.plot(old_x, old_y, label='Wafer 000', linestyle='None', marker='o')
plt.plot(new_x, new_y, label='Wafer 001', linestyle='None', marker='o')
plt.xlabel('Original Thickness [nm]')
plt.ylabel('Original Rs [ohms]')
plt.title('Resistance vs Thickness')
plt.legend()
plt.show()'''
