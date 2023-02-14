import scipy.io
import matplotlib.pyplot as plt
import numpy as np

summary = scipy.io.loadmat('data/DAQ/summary.mat')

eq_potentials = summary['equilibrium_potentials']
peak_heights = summary['peak_heights']

eq_potentials = []
peak_heights = []
labels = []
for pot, height, label in zip(summary['equilibrium_potentials'][0], 
  summary['peak_heights'][0], summary['labels'][0]):
    eq_potentials.append(pot[0][0])
    peak_heights.append(height[0][0])
    labels.append(label[0])
print(labels)

bad_indices = []
for i, potential in enumerate(eq_potentials):
    if potential > 0:
        bad_indices.append(i)

for i in np.flip(bad_indices):
    eq_potentials.pop(i)
    peak_heights.pop(i)
    labels.pop(i)

print(labels[8])
print(peak_heights[8])
print(eq_potentials[8])

plt.scatter(peak_heights, eq_potentials)
plt.show()