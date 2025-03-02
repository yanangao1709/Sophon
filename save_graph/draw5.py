# -------------------------Figure 13----------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Config import QNConfig
from QNEnv import QNModel
import matplotlib.ticker as mtick
import random
from Topology import RouteGenerator

def take_mean_value1(y):
    y_new = []
    for i in range(2):
        y_new.append(sum(y[0:2])/2)
    for t in range(0, 8):
        y_new.append(sum(y[t:t+2]) / 2)
    for t in range(0, len(y)-10):
        y_new.append(sum(y[t:t+10])/10)
    return y_new

def take_mean_value(y):
    y_new = []
    for t in range(len(y)):
        if t < 5:
            y_new.append(sum(y[0:5]) / 5)
        else:
            y_new.append(sum(y[:t + 1]) / (t + 1))
    return y_new

def draw_fidelity_threshold():
    data_fidelity = pd.read_csv("..\\Comparison\\results\\adjust_threshold_fidelity.csv")
    x = data_fidelity["fidelity_threshold"]
    average_data_fidelity_fixed = take_mean_value(data_fidelity['SophonFixed'])
    average_data_fidelity_flexible = take_mean_value(data_fidelity['SophonFlexible'])

    fig = plt.figure(figsize=(6.4, 4.8), dpi=80)
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    line1, = ax.plot(x[:], average_data_fidelity_fixed, color='b', linestyle='solid', marker='d',
             markerfacecolor='none', markevery=1,
             label='Sophon_Fixed')
    line2, = ax2.plot(x[:], average_data_fidelity_flexible, color='#BE2A2C', linestyle='dotted', marker='o',
             markerfacecolor='none', markevery=1,
             label='Sophon_Flexible')

    # x_tick_label = [i for i in range(16, 37, 5)]
    # ax.set_xticks(x_tick_label)
    ax.tick_params(labelsize=13)
    ax.tick_params(axis='y', colors='b', labelsize=13)
    ax2.xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    ax.set_xlabel('Fidelity thresholds', fontsize=17)  # X轴标签
    ax.set_ylabel("Total transmission times", fontsize=17)  # Y轴标签
    # ax2.set_ylabel("Total transmission times", fontsize=17)  # Y轴标签
    ax2.tick_params(axis='y', colors='#BE2A2C', labelsize=13)
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, fontsize=15)

    plt.gcf().subplots_adjust(left=0.11, bottom=0.12, right=0.88)
    # plt.gcf().subplots_adjust(left=0.1, right=0.8)
    plt.grid()
    plt.show()

def draw_delay_threshold():
    data_delay = pd.read_csv("..\\Comparison\\results\\adjust_threshold_delay.csv")
    x = data_delay['delay_threshold']
    average_fixed_delay = take_mean_value(data_delay["SophonFixed"])
    average_flexible_delay = take_mean_value(data_delay["SophonFlexible"])

    fig = plt.figure(figsize=(6.4, 4.8), dpi=80)
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    line1, = ax.plot(x[:], average_fixed_delay, color='b', linestyle='solid', marker='d',
            markerfacecolor='none', markevery=1,
            label='Sophon_Fixed')
    line2, = ax2.plot(x[:], average_flexible_delay, color='#BE2A2C', linestyle='dotted', marker='o',
             markerfacecolor='none', markevery=1,
             label='Sophon_Flexible')

    x_tick_label = [i for i in range(16, 37, 5)]
    ax.set_xticks(x_tick_label)
    ax.tick_params(labelsize=13)
    ax.tick_params(axis='y', colors='b', labelsize=13)
    ax2.xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    ax.set_xlabel('Delay thresholds', fontsize=17)  # X轴标签
    ax.set_ylabel("Total transmission times", fontsize=17)  # Y轴标签
    # ax2.set_ylabel("Total transmission times", fontsize=17)  # Y轴标签
    ax2.tick_params(axis='y', colors='#BE2A2C', labelsize=13)
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, fontsize=15)

    plt.gcf().subplots_adjust(left=0.13, bottom=0.12, right=0.9)
    # plt.gcf().subplots_adjust(left=0.1, right=0.8)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    draw_fidelity_threshold()
    draw_delay_threshold()