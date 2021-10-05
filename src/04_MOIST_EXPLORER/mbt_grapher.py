import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

PROBE_MAX = 3500    # max value obtained after testing probe in FULL DRY condition
PROBE_MIN = 1200    # min value obtained after testinf probe in FULL WET condition 


def moist_percent(reading, probe_max=PROBE_MAX, probe_min=PROBE_MIN):
    '''compute percent humidity from probe readings'''
    return 100 - ((reading - probe_min) * 100 / (probe_max - probe_min))



class MBTPlot():
    def __init__(self):
            
        # Constant definition
        self.N_SAMPLE = 1000  # samples tail to display

        mpl.rcParams['font.size'] = 8
        plt.style.use('dark_background') # previous was 'dark_background'
        fig = plt.figure()
        #mpl.rcParams['font.family'] = 'Courier New'
        # Read moisture data file
        # last file used was: "/mnt/moist_data_sens_pwroff_02.csv"
        # now changing to 
        self.data = pd.read_csv("/home/pi/uPY-PROJECTS/moistnet/05_DATA_FILEs/moist_data.csv",
                           names=['DATE', 'NODE', 'TEMP', 'CAT_1', 'CAT_2', 'PROBE_1', 'PROBE_2', 'VOLT', 'MAMP'],
                           parse_dates=[0])

        # Set DATE column as the new dataframe index
        self.data.set_index('DATE', inplace=True)

        # Extract only the last N samples from the dataframe
        self.df =self.data.iloc[-self.N_SAMPLE:]
        self.NODE_LIST = sorted(self.df.NODE.unique())    # Node List
        self.N_NODES = len(self.NODE_LIST)
        self.y_node = list()
        self.x_node = list()

    def plotTimeSeries(self):
        for i in range(self.N_NODES):
            self.y_node.append(self.df[self.df['NODE'] == self.NODE_LIST[i]])
            self.x_node.append(self.y_node[i].index)
            idx = i + 1
            plt.subplots_adjust(left=0.06, bottom=0.1, right=0.96, top=0.95,
                            wspace=0.20, hspace=0.30)
            # MOISTURE PLOT
            plt.subplot(4, self.N_NODES, idx)
            plt.title('NODE {}'.format(self.NODE_LIST[i]))
            plt.xticks(rotation=30)
            plt.ylabel('moisture [ % ]')
            plt.ylim(0, 100)
            plt.plot(self.x_node[i], moist_percent(self.y_node[i].PROBE_1), color='red', marker='x', markersize=2, label='probe 1', alpha=0.8)
            plt.plot(self.x_node[i], moist_percent(self.y_node[i].PROBE_2), color='orange', marker='x', markersize=2, label='probe 2', alpha=0.8)
            plt.fill_between(self.x_node[i], moist_percent(self.y_node[i].PROBE_1), color="red", alpha=0.2)
            plt.fill_between(self.x_node[i], moist_percent(self.y_node[i].PROBE_2), color="orange", alpha=0.2)
            plt.legend(loc='best')
            #plt.tight_layout()
            plt.grid(True, alpha=0.4, linestyle='dotted', linewidth=1)

            # VOLTAGE PLOT
            plt.subplot(4, self.N_NODES, idx + self.N_NODES)
            plt.xticks(rotation=30)
            plt.ylabel('battery [ V ]')
            plt.ylim(3.0, 4.3)

            plt.plot(self.x_node[i], self.y_node[i].VOLT, color='blue', marker='x', markersize=2, label='pod 1', alpha=0.8)
            plt.grid(True, alpha=0.4, linestyle='dotted', linewidth=1)
            plt.axhline(y=3.9, color='green', alpha=0.2)
            plt.axhline(y=3.8, color='yellow', alpha=0.2)
            plt.axhline(y=3.7, color='orange', alpha=0.2)
            plt.axhline(y=3.6, color='red', alpha=0.2)

            # CURRENT PLOT
            plt.subplot(4, self.N_NODES, idx + 2*self.N_NODES)
            plt.xticks(rotation=30)
            plt.ylabel('consumption [ mA ]')
            #plt.ylim(-100, 100)
            plt.plot(self.x_node[i], self.y_node[i].MAMP, color='green', marker='x', markersize=2, label='pod 1', alpha=0.8)
            plt.grid(True, alpha=0.4, linestyle='dotted', linewidth=1)
            
            # TEMPERATURE PLOT
            plt.subplot(4, self.N_NODES, idx + 3*self.N_NODES)
            plt.xticks(rotation=30)
            plt.ylabel('soil temperature [ Celsius ]')
            #plt.ylim(-100, 100)
            plt.plot(self.x_node[i], self.y_node[i].TEMP, color='cyan', marker='x', markersize=2, label='temp probe', alpha=0.8)
            plt.grid(True, alpha=0.4, linestyle='dotted', linewidth=1)

        #plt.savefig('moist.png')ù
        plt.show()

