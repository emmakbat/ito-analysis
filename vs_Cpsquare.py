import csv 
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

filename = 'ITOSA.csv'

class ItoData:
    def __init__(self, id, time, area, delta_L, delta_a, delta_b, coulombs, cps, current, Ri=None, Rf=None, Rchange=None):
        self.id = id 
        self.time = time
        self.area = area
        self.delta_L = delta_L
        self.delta_a = delta_a
        self.delta_b = delta_b
        self.coulombs = coulombs
        self.cps = cps
        self.Ri = Ri
        self.Rf = Rf
        self.Rchange=Rchange
        self.current = current

        self.sample_set = int(id[5])

def read_ito(filename):
    with open(filename) as csvfile:
        read = csv.reader(csvfile)
        # skip first row which is labels
        next(read)

        samples = []

        for row in read:
            id = row[0]
            time = int(row[1])
            area = float(row[2])
            delta_L = float(row[3])
            delta_a = float(row[4])
            delta_b = float(row[5])
            try:
                Ri = float(row[6])
                Rf = float(row[7])
                Rchange = float(row[8])
            except:
                Ri = None
                Rf = None
                Rchange = None
            coulombs = float(row[9])
            cps = float(row[10])
            current = int(row[11])

            samples.append(ItoData(id, time, area, delta_L, delta_a, 
            delta_b, coulombs, cps, current, Ri, Rf, Rchange))

    return samples 

def fitting(sample_list_x, sample_list_y):
    pL = Polynomial.fit(sample_list_x, [y[0] for y in sample_list_y], 2)
    pa = Polynomial.fit(sample_list_x, [y[1] for y in sample_list_y], 2)
    pb = Polynomial.fit(sample_list_x, [y[2] for y in sample_list_y], 2)

    return pL, pa, pb


samples = read_ito(filename)

reference_samples_x = []
reference_samples_y = []
reproducibility_x = []
reproducibility_y = []
high_current_x = []
high_current_y = []

for sample in samples:
    if sample.sample_set == 2:
        reference_samples_x.append(sample.cps)
        reference_samples_y.append((sample.delta_L, sample.delta_a, sample.delta_b))
    elif sample.current == 300:
        reproducibility_x.append(sample.cps)
        reproducibility_y.append((sample.delta_L, sample.delta_a, sample.delta_b))
    elif sample.current == 600:
        high_current_x.append(sample.cps)
        high_current_y.append((sample.delta_L, sample.delta_a, sample.delta_b))

pLref, paref, pbref = fitting(reference_samples_x, reference_samples_y)
pLrep, parep, pbrep = fitting(reproducibility_x, reproducibility_y)
pLhigh, pahigh, pbhigh = fitting(high_current_x, high_current_y)

plt.plot(reference_samples_x, reference_samples_y, 'o', label='ITOSA2')

# allows reset of color cycle
plt.gca().set_prop_cycle(None)
plt.plot(*pLref.linspace())
plt.plot(*paref.linspace())
plt.plot(*pbref.linspace())

plt.gca().set_prop_cycle(None)
plt.plot(reproducibility_x, reproducibility_y, 'v', label='Reproducibility test')

plt.gca().set_prop_cycle(None)
plt.plot(high_current_x, high_current_y, 's', label='600 uA')

plt.legend()
plt.show()        

