from scipy.io import loadmat
from scipy.stats import linregress 
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import statistics
from scipy.signal import savgol_filter
import numpy as np
from nk_helpers import colorFader
from plot_setup import plot_setup

plot_setup()

cg2 = '#d4ad9d'
cg1 = '#4a352f'

# from https://personal.sron.nl/~pault/
YlOrBr = np.flip(['#FB9A29', '#EC7014', '#CC4C02', '#993404', '#662506'])

labels = ['2000 um', '1000 um', '500 um', '250 um', '100 um']
widths = [0.25, 0.5, 1, 2] # mm
ics = [3.2, 5.8, 6.9, 7.6] # mA
linestyles = [':', '-.', '--', '-', ':']
filenames = ['Isw_curve 2022-05-20 14-15-13 ITO_wires_W1_T=1p3.mat',
            'Isw_curve 2022-05-20 14-31-28 ITO_wires_W5_T=1p3.mat', 
            'Isw_curve 2022-05-20 14-24-10 ITO_wires_W3_T=1p3.mat',
            'Isw_curve 2022-05-20 14-28-46 ITO_wires_W4_T=1p3.mat',
            'Isw_curve 2022-05-20 14-22-26 ITO_wires_W2_T=1p3.mat'
            ]

FILEPATH = 'data/patterned_widewires/'
# Tc filenames
filename = filenames[0]
#filename2 = 'Isw_curve 2022-05-11 15-20-16 Emma_piece_.mat'
iv = True
fourpoint = True

#FILM_FILEPATH = 'data/Tc_data/'
#film_filename = 'Isw_curve 2022-03-17 12-48-47 Emma_ITO_SA5E1_.mat'
#film2_filename = 'Isw_curve 2022-03-24 17-21-07 Emma_ITO_SA5D2_.mat'

'''
# iv (comment this out for Tc plotting)
filename = 'Isw_curve 2022-04-15 14-40-56 ITOmill_1_iv__T=300mK.mat'
iv = True'''



plot_widths = np.linspace(min(widths), max(widths), 300)
spl = make_interp_spline(widths, ics, k=2)
smooth_ic = spl(plot_widths)

plt.plot(plot_widths, smooth_ic, color='black', linestyle='--')
#plt.scatter(widths, ics, color='black')
for i, point in enumerate(widths):
    plt.scatter(point, ics[i], color=np.flip(YlOrBr)[i+1])
plt.xlabel('Width [mm]')
plt.ylabel('Isw [mA]')
plt.show()

def moving_average(data, window_width):
    cumsum_vec = np.cumsum(np.insert(data, 0, 0)) 
    ma_vec = (cumsum_vec[window_width:] - cumsum_vec[:-window_width]) / window_width
    return ma_vec

def get_tc_data(filename, num_points=100):
    tc_data = loadmat(filename)
    t_device = tc_data['T_device'][0]
    r_device = tc_data['R_device'][0]

    t, r = zip(*sorted(zip(t_device, r_device)))
    contact_resistance = statistics.mean(r[:num_points])

    return t, r, contact_resistance

if iv:
    for i, (filename, label) in enumerate(zip(filenames, labels)):
        iv_data = loadmat(FILEPATH+filename)
        i_device = iv_data['I_device'][0]
        v_device = iv_data['V_device'][0]

        plt.plot(v_device, [xi * 1000 for xi in i_device], label=label, color=YlOrBr[i])#, color=colorFader(cg1, cg2, i/(len(labels)-1)))
        #plt.scatter(v_device, [xi * 1000 for xi in i_device], color='black')
        plt.xlabel('Voltage [V]')
        plt.ylabel('Current [mA]')
    plt.legend()
    plt.show()

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
else:
    t, r, contact_resistance = get_tc_data(FILEPATH+filename, 20)
    t2, r2, contact_resistance2 = get_tc_data(FILEPATH+filename2, 20)
    #film_t, film_r, film_contact = get_tc_data(FILM_FILEPATH+film_filename)
    #film2_t, film2_r, film2_contact = get_tc_data(FILM_FILEPATH+film2_filename, 10)

    lossless_r = [ri - contact_resistance for ri in r]
    lossless_r2 = [ri - contact_resistance2 for ri in r2]
    #lossless_film = [ri - film_contact for ri in film_r]
    #lossless_film2 = [ri - film2_contact for ri in film2_r]

    norm_r = [ri/lossless_r[-1] for ri in lossless_r]
    norm_r2 = [ri/lossless_r2[-1] for ri in lossless_r2]
    #norm_rfilm = [ri/lossless_film[-1] for ri in lossless_film]
    #norm_rfilm2 = [ri/lossless_film2[-1] for ri in lossless_film2]

    lightgreen = '#66c2a5'
    darkgreen = '#488a75'
    lightblue = '#8da0cb'
    darkblue = '#687696'
    lightorange = '#fc8d62'
    darkorange = '#ba6849'

    #plt.scatter(t, norm_r, s=8, color=lightgreen, marker='d', label='2 mm')
    plt.scatter(t2, norm_r2, s=30, color=lightblue, marker='.', label='0.5 mm')
    #plt.scatter(film_t, norm_rfilm, s=5, color=lightorange, label='ITOSA5 E1 (120 s, 31 mC/cm^2)')
    #plt.scatter(film2_t, norm_rfilm2, s=5, label='ITOSA5 D2 (210 s, 33 mC/cm^2)')

    window_width = 5
    ma_t = moving_average(t, window_width)
    ma_r = moving_average(norm_r, window_width)
    window_width = 5
    split = 38
    ma_t2 = moving_average(t2, window_width)
    ma_r2 = moving_average(norm_r2, window_width)
    '''window_width=10
    ma_t2_high = moving_average(t2[split:], window_width)
    ma_r2_high = moving_average(lossless_r2[split:], window_width)
    ma_t2 = np.concatenate((ma_t2_low, ma_t2_high))
    ma_r2 = np.concatenate((ma_r2_low, ma_r2_high))'''

    #ma_filmt = moving_average(film_t, 50)
    #ma_filmr = moving_average(norm_rfilm, 50)

    #plt.plot(ma_t, ma_r, color=darkgreen)
    plt.plot(ma_t2, np.concatenate((savgol_filter(ma_r2[:split], 21, 3), savgol_filter(ma_r2[split:], 51, 4))), color=darkblue)
    #plt.plot(ma_filmt, ma_filmr, color=darkorange)
    plt.xlabel('Temperature [K]')
    plt.ylabel('Normalized Resistivity [Ohm]')
    plt.legend()
    plt.show()