# -------------------------Figure 11----------------------------
import pandas as pd
import matplotlib.pyplot as plt
from Config import QNConfig
from QNEnv import QNModel
import matplotlib.ticker as mtick
import random
from Topology import RouteGenerator

def take_mean_value1(y):
    y_new = []
    for i in range(20):
        y_new.append(sum(y[0:20])/20)
    for t in range(0, 180):
        y_new.append(sum(y[t:t+20]) / 20)
    for t in range(0, len(y)-200):
        y_new.append(sum(y[t:t+200])/200)
    return y_new

def take_mean_value(y):
    y_new = []
    for t in range(len(y)):
        if t < 5:
            y_new.append(sum(y[0:5]) / 5)
        else:
            y_new.append(sum(y[:t + 1]) / (t + 1))
    return y_new

def draw_Sophon_optimal1():
    data = pd.read_csv("global_rewards-optimal.csv")
    x = [i for i in range(len(data['episode']))]
    avg_Sophon_episode_reward = take_mean_value(data['episode_rewards'])
    average_request_Sophon_episode_reward = []
    for ix in x:
        average_request_Sophon_episode_reward.append(avg_Sophon_episode_reward[ix] / 1)

    data2 = pd.read_csv("global_rewards--5-0.001.csv")
    avg_Sophon_episode_reward2 = take_mean_value(data2['episode_rewards'])
    average_request_Sophon_episode_reward2 = []
    for ix in x:
        average_request_Sophon_episode_reward2.append(avg_Sophon_episode_reward2[ix] / 1)

    plt.plot(x[:], data['episode_rewards'][:], color='b', linestyle = 'solid', marker='d', markerfacecolor='none', markevery=400,
             label='Sophon_route_Optimal', linewidth=2)
    plt.plot(x[:], data2['episode_rewards'][:], color='#BE2A2C', linestyle = 'dashed', marker='o', markerfacecolor='none', markevery=400,
             label='Sophon', linewidth=2)

    plt.gca().xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Number of completed requests", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_Sophon_optimal2():
    data = pd.read_csv("global_rewards-optimal.csv")
    x = [i for i in range(len(data['episode']))]
    avg_Sophon_episode_reward = take_mean_value(data['max_obj'])
    average_request_Sophon_episode_reward = []
    for ix in x:
        average_request_Sophon_episode_reward.append(avg_Sophon_episode_reward[ix]+50 / 1)

    data2 = pd.read_csv("global_rewards--5-0.001.csv")
    avg_Sophon_episode_reward2 = take_mean_value(data2['max_obj'])
    average_request_Sophon_episode_reward2 = []
    for ix in x:
        average_request_Sophon_episode_reward2.append(avg_Sophon_episode_reward2[ix]+50 / 1)

    plt.plot(x[:], average_request_Sophon_episode_reward[:], color='b', linestyle = 'solid', marker='d', markerfacecolor='none', markevery=400,
             label='Sophon_route_Optimal', linewidth=2)
    plt.plot(x[:], average_request_Sophon_episode_reward2[:], color='#BE2A2C', linestyle = 'dashed', marker='o', markerfacecolor='none', markevery=400,
             label='Sophon', linewidth=2)

    plt.gca().xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Total throughput (qubits)", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    draw_Sophon_optimal1()
    draw_Sophon_optimal2()