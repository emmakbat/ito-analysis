import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

filepath = 'Sample-000c/EDS_1014/'
filenames = [
    '1014 SI HAADF 125 kx_profile-Au.txt', 
    '1014 SI HAADF 125 kx_profile-Pt.txt',
    '1014 SI HAADF 125 kx_profile-In.txt', 
    '1014 SI HAADF 125 kx_profile-Sn.txt',
    '1014 SI HAADF 125 kx_profile-Na.txt', 
    '1014 SI HAADF 125 kx_profile-O.txt',
    '1014 SI HAADF 125 kx_profile-Si.txt'
    ]

labels = ['Gold', 'Platinum', 'Indium', 'Tin', 'Sodium', 'Oxygen', 'Silicon']
linestyles = [':', ':', '--', '-', '-', '--', '-.']

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

plot_setup(fig_y=7.2*4/5)

def read_EDS_HAADF(filename):
    x = []
    y = []
    with open(filename) as f:
        read_data = f.read().splitlines()
        for line in read_data:
            words = line.split(';')
            x.append(float(words[0])*10**9)
            y.append(float(words[1]))
    return x, y 

def colorFader(c1, c2, mix=0):
    '''
    credit to Markus Dutschke on Stack Overflow for this one
    '''
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

colors = [colorFader('darkgray', 'black', i/len(labels[1:])) for i in range(len(labels))]
print(colors)
colors[4] = 'springgreen'

colors = ['#a89e79', '#8d8d8d', '#4e5f73', '#345249', '#f5462f', '#130b1a', '#000000']
colors = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB']

for color, linestyle, label, filename in zip(colors, linestyles, labels, filenames):
    x, y = read_EDS_HAADF(filepath + filename)
    plt.plot(x, y, label=label, linestyle=linestyle, color=color)

'''
plt.axvline(48) # silicon edge
plt.axvline(160) # surface edge
plt.axvline(200) # nanoparticle edge'''

plt.xlabel('Position [nm]')
plt.ylabel('Intensity [counts]')
plt.legend()
plt.savefig('eds_haadf.svg')
plt.show()