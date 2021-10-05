import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import config_pod as cfg
from datetime import datetime


# TODO: must get PROBE MAX and MIN values directly from the real dataframe. then perform acheck for max and min vals, to double check validity *can-t be less than zero nor greater than 4000


# Function definitions
    
def moist_percent(reading, probe_max=cfg.PROBE_MAX, probe_min=cfg.PROBE_MIN):
    '''compute percent humidity from probe readings'''
    return 100 - ((reading - probe_min) * 100 / (probe_max - probe_min))

mpl.rcParams['font.size'] = 8
plt.style.use('dark_background') # previous was 'dark_background'


class Pod():
    def __init__(self):
        print(".")
        pod_df = pd.read_csv(cfg.DATA_FILE,
                           names=['DATE', 'POD_ID', 'TEMP', 'CAT_1', 'CAT_2', 'PROBE_1', 'PROBE_2', 'VOLT', 'MAMP'],
                           parse_dates=[0])

        self.clean_df = pod_df.drop(['CAT_1', 'CAT_2'], axis=1)
        self.clean_df['DAY'] = self.clean_df['DATE'].dt.day
        self.clean_df['HOUR'] = self.clean_df['DATE'].dt.hour
        self.clean_df["PIZZA"] = self.clean_df["DATE"].dt.strftime("%Y-%m-%d")
        self.clean_df[['P1%', 'P2%']] = moist_percent(self.clean_df[['PROBE_1', 'PROBE_2']])
        
        self.clean_df.set_index('DATE', inplace=True)

        self.POD_LIST = sorted(pod_df['POD_ID'].unique())    # Node List
        self.N_PODS = len(self.POD_LIST)

    def get_pod_hourly_data(self, pod_id=1):
        if pod_id in self.POD_LIST:
            
            return self.clean_df[self.clean_df['POD_ID']==pod_id]
        else:
            print("ERR: INVALID POD ID")
            return None

    def generate_probe_xtab(self, pod_id=1, probe_id=1, sd=datetime.now(), ed=datetime.now()):
        n = self.get_pod_hourly_data(pod_id)[sd:ed]
        
        if probe_id == 1:
            probe = 'P1%'
        elif probe_id == 2:
            probe = 'P2%'
        else:
            print('ERR: WRONG PROBE ID')
        xtab_probe = pd.crosstab(n["PIZZA"], n["HOUR"], values=n[probe], aggfunc="median").round(1)
        x = xtab_probe.fillna(axis=1, method='bfill')#.fillna(axis=1, method='ffill')
        return x

    def display_pod_timeseries(self, pod_list=[1], days=cfg.DAYS):
        #fig = plt.figure()
        fig, ax = plt.subplots(4, 5, sharex='col', sharey='row')
        plt.xticks(rotation=30)
 
        ts = pd.Timestamp(datetime.now())
        td = ts - pd.Timedelta(days=days)
       
        idx = 0
        for i in range(4):
            for j in range(5):
                if idx < len(pod_list):
                    data = self.get_pod_hourly_data(pod_list[idx])[td:ts]                 
                    ax[i, j].plot(data.index, moist_percent(data.PROBE_1), 
                        color='red', marker='x', markersize=2, label='probe_1', alpha=0.8)                 
                    ax[i, j].plot(data.index, moist_percent(data.PROBE_2), 
                        color='orange', marker='x', markersize=2, label='probe_2', alpha=0.8)
                    ax[i, j].fill_between(data.index, moist_percent(data.PROBE_1), color='red', alpha=0.2)
                    ax[i, j].fill_between(data.index, moist_percent(data.PROBE_2), color='orange', alpha=0.2)
                    ax[i, j].set_title("NODE {}".format(pod_list[idx]))
                ax[i, j].set_ylim([0, 100])
                ax[i, j].legend(loc='best')
                for k in ax[i, j].get_xticklabels():
                    k.set_rotation(30)
                ax[i, j].grid(True, alpha=0.4, linestyle='dotted', linewidth=1)
                idx += 1
            idx += 1
        plt.show()

    def display_pod_heatmap(self, pod_list=[1, 2], sd=datetime.now(), ed=datetime.now()):
        fig, ax = plt.subplots(nrows=len(pod_list), ncols=2, sharex='row', sharey='row')
        i=0
        for j in pod_list:
            probe1 = sns.heatmap(self.generate_probe_xtab(j, 1, sd, ed), 
                    annot=True, vmin=0, vmax=100, cmap='YlGnBu', ax=ax[i,0])   
            ax[i, 0].set_title("PROBE 1")
            ax[i, 0].set_ylabel("POD {}".format(j))
            probe2 = sns.heatmap(self.generate_probe_xtab(j, 2, sd, ed), 
                    annot=True, vmin=0, vmax=100, cmap='YlGnBu', ax=ax[i,1])   
            ax[i, 1].set_title("PROBE 2")
            ax[i, 1].set_ylabel("POD {}".format(j))
            i+=1
        plt.show()

    def plot_mbt(self, pod_list=[1, 2], sd=datetime.now(), ed=datetime.now()):
        fig, ax = plt.subplots(4, len(pod_list), sharex='all', sharey='row')
        plt.subplots_adjust(top=0.968, bottom=0.075, left=0.036, right=0.985, hspace=0.057, wspace=0.025)
        plt.xticks(rotation=30)

        idx = 0

        for j in range(len(pod_list)):
            data = self.get_pod_hourly_data(sorted(pod_list)[idx])[sd:ed]
            # MOISTURE PLOT
            if idx < len(pod_list):
                ax[0, j].plot(data.index, moist_percent(data.PROBE_1), 
                    color='red', marker='x', markersize=2, label='probe_1', alpha=0.8)                 
                ax[0, j].plot(data.index, moist_percent(data.PROBE_2), 
                    color='orange', marker='x', markersize=2, label='probe_2', alpha=0.8)
                ax[0, j].fill_between(data.index, moist_percent(data.PROBE_1), color='red', alpha=0.2)
                ax[0, j].fill_between(data.index, moist_percent(data.PROBE_2), color='orange', alpha=0.2)
                ax[0, j].set_title("NODE {}".format(pod_list[idx]))
                ax[0, j].set_ylabel('moisture [ % ]')
                ax[0, j].set_ylim([0, 100])
                ax[0, j].legend(loc='best')
                ax[0, j].grid(True, alpha=0.4, linestyle='dotted', linewidth=1)
            
                # BATTERY VOLTAGE PLOT
                ax[1, j].plot(data.index, data.VOLT, color='blue', marker='x', markersize=2,
                        label='pod X', alpha=0.8)
                ax[1, j].set_ylim([3.0, 4.3])
                ax[1, j].set_ylabel('battery [ V ]')
                ax[1, j].grid(True, alpha=0.4, linestyle='dotted', linewidth=1)
                #ax[1, j].axhline(y=3.9, color='green', alpha=0.2)
                #ax[1, j].axhline(y=3.8, color='yellow', alpha=0.2)
                ax[1, j].axhline(y=3.7, color='orange', alpha=0.2)
                ax[1, j].axhline(y=3.6, color='red', alpha=0.2)
            
                # CURRENT DRAW PLOT
                ax[2, j].set_ylabel('consumption [ mA ]')
                ax[2, j].plot(data.index, data.MAMP, color='green', marker='x', markersize=2,
                        label='pod X', alpha=0.8)
                ax[2, j].grid(True, alpha=0.4, linestyle='dotted', linewidth=1)

                # TEMPERATURE PROBE PLOT
                ax[3, j].set_ylabel('temperature [ Celsius]')
                ax[3, j].plot(data.index, data.TEMP, color='cyan', marker='x', markersize=2,
                        label='temp probe', alpha=0.8)
                ax[3, j].grid(True, alpha=0.4, linestyle='dotted', linewidth=1)

            for k in ax[3, j].get_xticklabels():
                k.set_rotation(30)
            idx += 1
        idx += 1
        plt.show()        

                







