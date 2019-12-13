from drake import lcmt_iiwa_status, lcmt_iiwa_command, lcmt_iiwa_info
lcm_channels = ["IIWA_INFO","_"]
sample_size = 500
frequency = 30


lcm_objects = []
currentValues = [0,0,0,0]
#currnetValue1 = 0
def callback(channel, msg):
    global lcm_channels
    if channel == "IIWA_INFO":
        newStatusMessage1 = lcmt_iiwa_info()
        currentValues[lcm_channels.index(channel)] = newStatusMessage1.decode(msg).joint_torque_external[1]

    elif channel == "IIWA_STATUS":
        newStatusMessage = lcmt_iiwa_status()
        currentValues[lcm_channels.index(channel)] = newStatusMessage.decode(msg).joint_torque_external[1]
        currentValues[lcm_channels.index(channel)+1] = newStatusMessage.decode(msg).joint_torque_measured[1] -newStatusMessage.decode(msg).joint_torque_commanded[1]
    elif channel == "IIWA_COMMAND":
        newMessage = lcmt_iiwa_command()
        currentValues[lcm_channels.index(channel)] = newMessage.decode(msg).joint_torque[1]


import time
from random import randint
# import pydrake.systems.lcm as mut
from lcm import LCM
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import fft

fig, axes = plt.subplots(len(lcm_channels),1)
x = [[],[],[],[]]
y = [[],[],[],[]]
#y2 = []
loop_time = 0

lcm_ = LCM()


def initPlots():
    index = 0
    lcmSub = lcm_.subscribe(lcm_channels[index], callback)
    lcmSub.set_queue_capacity(10)
    for ax in axes:
        ax.set_title(lcm_channels[index])
        index += 1

def runPlots(i):
    global loop_time, x, y, lcm_channels, lcm_, currentValues
    index = 0
    for ax in axes:
        x[index].append(loop_time)
        y[index].append(currentValues[index])
        #y2.append(currnetValue1)
        if len(x[index]) == sample_size:
            x[index].pop(0)
            y[index].pop(0)
            #y2.pop(0)
        # x[index] = x[-sample_size:]
        # y[index] = y[-sample_size:]
        axes[index].clear()
        axes[index].plot(x[index],y[index])
        #axes[index].plot(x[index],y2)
        index += 1
    loop_time += 1
    # if loop_time % 30:
    lcm_.handle()

def getLcmData(index):
    return currentValues[index] #randint(0,10)

if __name__ == "__main__":
    initPlots()
    ani = animation.FuncAnimation(fig, runPlots, interval=frequency)
    plt.show() 