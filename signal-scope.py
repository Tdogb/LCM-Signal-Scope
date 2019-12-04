import time
from random import randint
# from lcm import LCM

import matplotlib.pyplot as plt
import matplotlib.animation as animation

lcm_channels = ["TEST_CHANNEL1", "TEST_CHANNEL2", "TEST_CHANNEL3"]
sample_size = 20
frequency = 200

# fig = plt.figure()
fig, axes = plt.subplots(len(lcm_channels))
x = [[],[],[],[]]
y = [[],[],[],[]]
# axes = []
loop_time = 0

def initPlots():
    index = 0
    for ax in axes:
        ax.set_title(lcm_channels[index])
        index += 1

def runPlots(i):
    global loop_time, x, y, lcm_channels
    index = 0
    for ax in axes:
        x[index].append(loop_time)
        y[index].append(getLcmData(lcm_channels[index]))
        # x[index] = x[index,-sample_size:]
        # y[index] = y[index,-sample_size:]
        axes[index].clear()
        axes[index].plot(x[index],y[index])
        index += 1
    loop_time += 1

def getLcmData(channel):
    return randint(0,10)

if __name__ == "__main__":
    initPlots()
    ani = animation.FuncAnimation(fig, runPlots, interval=frequency)
    plt.show()