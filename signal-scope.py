import time
from random import randint
import pydrake.systems.lcm as mut
from drake import lcmt_iiwa_status, lcmt_iiwa_command
from lcm import LCM
import numpy as np
# from drake import lcm

import matplotlib.pyplot as plt
import matplotlib.animation as animation

lcm_channels = ["IIWA_COMMAND","_"]
lcm_objects = []
sample_size = 500
frequency = 30

fig, axes = plt.subplots(len(lcm_channels),1)
# axes = np.array(axes)
x = [[],[],[],[]]
y = [[],[],[],[]]
loop_time = 0

lcm_ = LCM()
currentValues = [0,0,0,0]

def callback(channel, msg):
    global lcm_channels
    if channel == "IIWA_STATUS":
        newMessage = lcmt_iiwa_status()
        currentValues[lcm_channels.index(channel)] = newMessage.decode(msg).joint_torque_external[1]
    elif channel == "IIWA_COMMAND":
        newMessage = lcmt_iiwa_command()
        currentValues[lcm_channels.index(channel)] = newMessage.decode(msg).joint_torque[1]
        currentValues[lcm_channels.index(channel)+1] = newMessage.decode(msg).joint_torque[0]

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
        if len(x[index]) == sample_size:
            x[index].pop(0)
            y[index].pop(0)
        # x[index] = x[-sample_size:]
        # y[index] = y[-sample_size:]
        axes[index].clear()
        axes[index].plot(x[index],y[index])
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