# -------------------------Figure 9----------------------------
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import FuncFormatter

def take_mean_value(y):
    y_new = []
    for t in range(len(y)):
        if t < 5:
            y_new.append(sum(y[0:5]) / 5)
        else:
            y_new.append(sum(y[:t + 1]) / (t + 1))
    return y_new

def draw_Sophon_train1():
    data = pd.read_csv("global_rewards--20-0.0001.csv")
    x = [i for i in range(len(data['episode']))]
    avg_Sophon_episode_reward = take_mean_value(data['episode_rewards'])
    average_request_Sophon_episode_reward = []
    for ix in x:
        average_request_Sophon_episode_reward.append(avg_Sophon_episode_reward[ix] / 1)

    data2 = pd.read_csv("global_rewards--15-0.0001.csv")
    avg_Sophon_episode_reward2 = take_mean_value(data2['episode_rewards'])
    average_request_Sophon_episode_reward2 = []
    for ix in x:
        average_request_Sophon_episode_reward2.append(avg_Sophon_episode_reward2[ix] / 1)

    data3 = pd.read_csv("global_rewards--10-0.0001.csv")
    avg_Sophon_episode_reward3 = take_mean_value(data3['episode_rewards'])
    average_request_Sophon_episode_reward3 = []
    for ix in x:
        average_request_Sophon_episode_reward3.append(avg_Sophon_episode_reward3[ix] / 1)

    data4 = pd.read_csv("global_rewards--5-0.001.csv")
    avg_Sophon_episode_reward4 = take_mean_value(data4['episode_rewards'])
    average_request_Sophon_episode_reward4 = []
    for ix in x:
        average_request_Sophon_episode_reward4.append(avg_Sophon_episode_reward4[ix] / 1)

    plt.plot(x[:], average_request_Sophon_episode_reward[:], color='b', linestyle = 'solid', marker='d', markerfacecolor='none', markevery=400,
             label='$|R|=20$')
    plt.plot(x[:], average_request_Sophon_episode_reward2[:], color='#BE2A2C', linestyle = 'dotted', marker='o', markerfacecolor='none', markevery=400,
             label='|R|=15')
    plt.plot(x[:], average_request_Sophon_episode_reward3[:], color='#35903A', linestyle = 'dashed', marker='s', markerfacecolor='none', markevery=400,
             label='|R|=10')
    plt.plot(x[:], average_request_Sophon_episode_reward4[:], color='#E47B26', linestyle = 'dashdot', marker='x', markerfacecolor='none', markevery=400,
             label='|R|=5')

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

def draw_Sophon_train2():
    data = pd.read_csv("global_rewards--20-0.0001.csv")
    x = [i for i in range(len(data['episode']))]
    avg_Sophon_episode_reward = take_mean_value(data['max_obj'])
    average_request_Sophon_episode_reward = []
    for ix in x:
        average_request_Sophon_episode_reward.append(avg_Sophon_episode_reward[ix] / 20)

    data2 = pd.read_csv("global_rewards--15-0.0001.csv")
    avg_Sophon_episode_reward2 = take_mean_value(data2['max_obj'])
    average_request_Sophon_episode_reward2 = []
    for ix in x:
        average_request_Sophon_episode_reward2.append(avg_Sophon_episode_reward2[ix] / 15)

    data3 = pd.read_csv("global_rewards--10-0.0001.csv")
    avg_Sophon_episode_reward3 = take_mean_value(data3['max_obj'])
    average_request_Sophon_episode_reward3 = []
    for ix in x:
        average_request_Sophon_episode_reward3.append(avg_Sophon_episode_reward3[ix] / 10)

    data4 = pd.read_csv("global_rewards--5-0.001.csv")
    avg_Sophon_episode_reward4 = take_mean_value(data4['max_obj'])
    average_request_Sophon_episode_reward4 = []
    for ix in x:
        average_request_Sophon_episode_reward4.append(avg_Sophon_episode_reward4[ix] / 5)

    plt.plot(x[:], avg_Sophon_episode_reward[:], color='b', linestyle='solid', marker='d', markerfacecolor='none',
             markevery=400,
             label='$|R|=20$')
    plt.plot(x[:], avg_Sophon_episode_reward2[:], color='#BE2A2C', linestyle='dotted', marker='o',
             markerfacecolor='none', markevery=400,
             label='|R|=15')
    plt.plot(x[:], avg_Sophon_episode_reward3[:], color='#35903A', linestyle='dashed', marker='s',
             markerfacecolor='none', markevery=400,
             label='|R|=10')
    plt.plot(x[:], avg_Sophon_episode_reward4[:], color='#E47B26', linestyle='dashdot', marker='x',
             markerfacecolor='none', markevery=400,
             label='|R|=5')

    plt.gca().xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Total transmitting data volume", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_Sophon_train3():
    data = pd.read_csv("global_rewards--20-0.0001.csv")
    x = [i for i in range(len(data['episode']))]
    avg_Sophon_episode_reward = take_mean_value(data['suc_datas'])

    data2 = pd.read_csv("global_rewards--15-0.0001.csv")
    avg_Sophon_episode_reward2 = take_mean_value(data2['suc_datas'])

    data3 = pd.read_csv("global_rewards--10-0.0001.csv")
    avg_Sophon_episode_reward3 = take_mean_value(data3['suc_datas'])

    data4 = pd.read_csv("global_rewards--5-0.001.csv")
    avg_Sophon_episode_reward4 = take_mean_value(data4['suc_datas'])

    plt.plot(x[:], avg_Sophon_episode_reward[:], color='b', linestyle='solid', marker='d', markerfacecolor='none',
             markevery=400,
             label='$|R|=20$')
    plt.plot(x[:], avg_Sophon_episode_reward2[:], color='#BE2A2C', linestyle='dotted', marker='o',
             markerfacecolor='none', markevery=400,
             label='|R|=15')
    plt.plot(x[:], avg_Sophon_episode_reward3[:], color='#35903A', linestyle='dashed', marker='s',
             markerfacecolor='none', markevery=400,
             label='|R|=10')
    plt.plot(x[:], avg_Sophon_episode_reward4[:], color='#E47B26', linestyle='dashdot', marker='x',
             markerfacecolor='none', markevery=400,
             label='|R|=5')

    plt.gca().xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Total data of completed requests", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(left=0.13)
    plt.grid()
    plt.show()

def draw_Sophon_train4():
    data = pd.read_csv("global_rewards--20-0.0001.csv")
    x = [i for i in range(len(data['episode']))]
    Sophon_max_obj = data['max_obj']
    Sophon_suc_datas = data['suc_datas']
    results = []
    for ix in x:
        results.append((Sophon_suc_datas[ix] / Sophon_max_obj[ix])/20)
    avg_results = take_mean_value(results)

    data2 = pd.read_csv("global_rewards--15-0.0001.csv")
    Sophon_max_obj2 = data2['max_obj']
    Sophon_suc_datas2 = data2['suc_datas']
    results2 = []
    for ix in x:
        results2.append((Sophon_suc_datas2[ix] / Sophon_max_obj2[ix])/15)
    avg_results2 = take_mean_value(results2)

    data3 = pd.read_csv("global_rewards--10-0.0001.csv")
    Sophon_max_obj3 = data3['max_obj']
    Sophon_suc_datas3 = data3['suc_datas']
    results3 = []
    for ix in x:
        results3.append((Sophon_suc_datas3[ix] / Sophon_max_obj3[ix])/10)
    avg_results3 = take_mean_value(results3)

    data4 = pd.read_csv("global_rewards--5-0.001.csv")
    Sophon_max_obj4 = data4['max_obj']
    Sophon_suc_datas4 = data4['suc_datas']
    results4 = []
    for ix in x:
        results4.append((Sophon_suc_datas4[ix] / Sophon_max_obj4[ix])/5)
    avg_results4 = take_mean_value(results4)

    plt.plot(x[:], avg_results[:], color='b', linestyle='solid', marker='d', markerfacecolor='none',
             markevery=400,
             label='$|R|=20$')
    plt.plot(x[:], avg_results2[:], color='#BE2A2C', linestyle='dotted', marker='o',
             markerfacecolor='none', markevery=400,
             label='|R|=15')
    plt.plot(x[:], avg_results3[:], color='#35903A', linestyle='dashed', marker='s',
             markerfacecolor='none', markevery=400,
             label='|R|=10')
    plt.plot(x[:], avg_results4[:], color='#E47B26', linestyle='dashdot', marker='x',
             markerfacecolor='none', markevery=400,
             label='|R|=5')

    plt.gca().xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Episodes', fontsize=17)
    plt.ylabel("Average Transmitting ratio", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(left=0.13)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    draw_Sophon_train1()
    draw_Sophon_train2()
    draw_Sophon_train3()
    draw_Sophon_train4()
