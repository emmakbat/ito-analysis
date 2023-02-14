from scipy.io import loadmat
from scipy.stats import linregress 
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import statistics
from scipy.signal import savgol_filter
import numpy as np
import matplotlib as mpl
from scipy.io import savemat

cg2 = '#d4ad9d'
cg1 = '#4a352f'

# from https://personal.sron.nl/~pault/
YlOrBr = np.flip(['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506'])

labels = ['2000 um', '1000 um', '500 um', '250 um', '100 um']
widths = [0.25, 0.5, 1, 2] # mm
ics = [3.2, 5.8, 6.9, 7.6] # mA (extracted from I-V plots produced below)
linestyles = [':', '-.', '--', '-', ':']
filenames = ['Isw_curve 2022-05-20 14-15-13 ITO_wires_W1_T=1p3.mat',
            'Isw_curve 2022-05-20 14-31-28 ITO_wires_W5_T=1p3.mat', 
            'Isw_curve 2022-05-20 14-24-10 ITO_wires_W3_T=1p3.mat',
            'Isw_curve 2022-05-20 14-28-46 ITO_wires_W4_T=1p3.mat',
            'Isw_curve 2022-05-20 14-22-26 ITO_wires_W2_T=1p3.mat'
            ]

FILEPATH = 'IV/'

filename = filenames[0]
filename2 = ''
iv = True
fourpoint = True

def colorFader(c1, c2, mix=0):
    '''
    credit to Markus Dutschke on Stack Overflow for this one
    '''
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

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

plot_widths = np.linspace(min(widths), max(widths), 300)
spl = make_interp_spline(widths, ics, k=2)
smooth_ic = spl(plot_widths)

plt.figure()
plt.gcf().subplots_adjust(bottom=0.2)
plt.plot(plot_widths, smooth_ic, color='black', linestyle='--')
#plt.scatter(widths, ics, color='black')
for i, point in enumerate(widths):
    plt.scatter(point, ics[i], color=np.flip(YlOrBr)[i+1])
plt.xlabel('Width [mm]')
plt.ylabel('Isw [mA]')
plt.savefig('Isw_vs_width.svg')
plt.show()

iv_dict = {}
for i, (filename, label) in enumerate(zip(filenames, labels)):
    iv_data = loadmat(FILEPATH+filename)
    i_device = iv_data['I_device'][0]
    v_device = iv_data['V_device'][0]
    print(label)

    plt.figure()
    plt.plot(v_device, [xi * 1000 for xi in i_device], label=label, color='black')#, color=colorFader(cg1, cg2, i/(len(labels)-1)))
    #plt.scatter(v_device, [xi * 1000 for xi in i_device], color='black')
    plt.xlabel('Voltage [V]')
    plt.ylabel('Current [mA]')
    plt.legend()
    plt.savefig(label+'_iv.svg')
    plt.show()
    iv_dict[label+'_i'] = i_device
    iv_dict[label+'_v'] = v_device
savemat('widewires_iv.mat', iv_data)

if not fourpoint:
    y, x = zip(*sorted(zip(v_device, i_device)))
    middle_linear_x = x[990:1010]
    middle_linear_y = y[990:1010]

    linear_x = middle_linear_x
    linear_y = middle_linear_y

    result = linregress(middle_linear_x, middle_linear_y)
    predicted_y = [xi*result.slope + result.intercept for xi in x]

    predicted_v = [xi - yi*1/result.slope for xi, yi in zip(x, y)]

    plt.plot(predicted_y, x)
    plt.scatter(middle_linear_y, middle_linear_x)
    plt.show()

    removed_linear = [yi - linear_yi for yi, linear_yi in zip(y, predicted_y)]
    plt.scatter(removed_linear, [xi * 1000 for xi in x], s=5)
    plt.xlabel('Voltage [V]')
    plt.ylabel('Current [mA]')
    plt.show()