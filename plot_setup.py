import matplotlib.pyplot as plt

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