import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Constant definition
N_SAMPLE = 100000    # Number of the last sample to extract for the entire dataframe

mpl.rcParams['font.size'] = 8
plt.style.use('dark_background')
fig = plt.figure()
#mpl.rcParams['font.family'] = 'Courier New'
# Read moisture data file
data = pd.read_csv("rpi_moist_data_TEMP-AND-SALINITY_TESTS_30-07.csv",
                   names=['DATE', 'NODE', 'MSEC', 'PROBE_1', 'PROBE_2', 'VOLT', 'MAMP'],
                   parse_dates=[0])

# Set DATE column as the new dataframe index
data.set_index('DATE', inplace=True)

# Extract only the last N samples from the dataframe
df = data.iloc[-N_SAMPLE:]

NODE_LIST = sorted(df.NODE.unique())    # Node List
N_NODES = len(NODE_LIST)
print(NODE_LIST)

y_node = list()
x_node = list()

for i in range(N_NODES):
    y_node.append(df[df['NODE'] == NODE_LIST[i]])
    x_node.append(y_node[i].index)
    print()
    print(y_node[i].describe().to_string())
    print()

    probe_error_node = np.abs(y_node[i].PROBE_2.describe() - y_node[i].PROBE_1.describe())
    print(probe_error_node)

    idx = i + 1

    plt.subplots_adjust(left=0.06, bottom=0.1, right=0.96, top=0.95,
                    wspace=0.20, hspace=0.30)

    # MOISTURE PLOT
    plt.subplot(3, N_NODES, idx)
    plt.title('NODE {}'.format(NODE_LIST[i]))
    plt.xticks(rotation=30)
    plt.ylabel('moist')
    plt.ylim(0, 650)
    plt.plot(x_node[i], y_node[i].PROBE_1, color='red', marker='x', label='probe 1', alpha=0.8)
    plt.plot(x_node[i], y_node[i].PROBE_2, color='orange', marker='x', label='probe 2', alpha=0.8)
    plt.fill_between(x_node[i], y_node[i].PROBE_1, color="red", alpha=0.2)
    plt.fill_between(x_node[i], y_node[i].PROBE_2, color="orange", alpha=0.2)
    plt.legend(loc='best')
    #plt.tight_layout()
    plt.grid(True, alpha=0.4, linestyle='dotted', linewidth=1)

    # VOLTAGE PLOT
    plt.subplot(3, N_NODES, idx + N_NODES)
    plt.xticks(rotation=30)
    plt.ylabel('battery [ V ]')
    plt.ylim(3.7, 4.3)

    plt.plot(x_node[i], y_node[i].VOLT, color='blue', marker='x', label='probe 1', alpha=0.8)
    plt.grid(True, alpha=0.4)
    plt.axhline(y=3.9, color='yellow', alpha=0.6)

    # CURRENT PLOT
    plt.subplot(3, N_NODES, idx + 2*N_NODES)
    plt.xticks(rotation=30)
    plt.ylabel('consumption [ mA ]')
    #plt.ylim(-100, 100)
    plt.plot(x_node[i], y_node[i].MAMP, color='green', marker='x', label='probe 1', alpha=0.8)
    plt.grid(True, alpha=0.4)

#plt.savefig('moist.png')ù
plt.show()

