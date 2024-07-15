import pandas as pd
import matplotlib.pyplot as plt
from Config import QNConfig


def take_mean_value(y):
    y_new = []
    for i in range(20):
        y_new.append(sum(y[0:20])/20)
    for t in range(0, 80):
        y_new.append(sum(y[t:t+20]) / 20)
    for t in range(0, len(y)-100):
        y_new.append(sum(y[t:t+100])/100)
    return y_new

# data = pd.read_csv("global_rewards.csv")
local_data = pd.read_csv("agent_local_rewards.csv")
# data3 = pd.read_csv("delay_thr-180.csv")
x = [i for i in range(1700)]
fig = plt.figure()
for agent_id in range(QNConfig.agent_num):
    agent_data = local_data[str(agent_id)][0:1700]
    # episode_rewards = data['episode_rewards']
    # max_obj = data['max_obj']
    # suc_datas = data['suc_datas']

    # for agent_id in range(QNConfig.agent_num):
    #     step_avg_data = [d for d in data2[str(agent_id)]]
    #     episode_reward = take_mean_value(step_avg_data)
    #     plt.plot(x, episode_reward, marker='o', markevery=150, color='m', linestyle='-', markerfacecolor='none', label='')
    plt.plot(x, take_mean_value(agent_data), marker='^', markevery=150, color='c', linestyle='-', markerfacecolor='none', label='')
    # plt.plot(x, episode_reward3, marker='s', markevery=150, color='y', linestyle='dashed', markerfacecolor='none', label='$\Gamma^{thr}=180$')
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=17)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Average episode reward", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()