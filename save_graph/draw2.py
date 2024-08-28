# -------------------------Figure 10----------------------------
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

def generate_a_request():
    s_r = random.randint(0, QNConfig.node_num)
    if s_r != QNConfig.node_num:
        s_r += 1
    d_r = random.randint(0, QNConfig.node_num)
    if d_r != QNConfig.node_num:
        d_r += 1
    if s_r == d_r:
        s_r = 1
        d_r = 11
    return [s_r, d_r]

def obtain_node_importance():
    frequency = 100
    total_node_importance = {key: [0 for f in range(frequency)] for key in range(QNConfig.node_num)}
    for f in range(frequency):
        request_number = 50
        # 按照问题规模和设置，随机生成20个请求
        requests = []
        candidates_routes = []
        for r_i in range(request_number):
            new_r = generate_a_request()
            requests.append(new_r)
            # 获取每个请求对候选路径，并存储
            routes_info = RouteGenerator.generate_routes(new_r, False)
            candidates_routes.append(routes_info[1])
        # 计算每个节点的重要程度，即在当前设置规模下，被用到的次数
        for r_i in range(request_number):
            r_routes = candidates_routes[r_i]
            for rt in range(QNConfig.candidate_route_num):
                for n in range(QNConfig.node_num):
                    route = r_routes[rt]
                    if (n+1 in route) and (n+1 != route[0]) and (n+1 != route[-1]):
                        total_node_importance[n][f] += 1
                        break
    node_importance = {key: 0 for key in range(QNConfig.node_num)}
    for n in range(QNConfig.node_num):
        node_importance[n] = sum(total_node_importance[n])/frequency
    return node_importance

def draw_node_importance(importance):
    x = [i for i in range(QNConfig.node_num)]
    node_importance = [importance[n] for n in range(QNConfig.node_num)]

    fig = plt.figure(figsize=(6.4, 4.8), dpi=80)
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    for i, v in enumerate(node_importance):
        if i in [4,5,10]:
            ax.bar(i, v, color='#F9E400', hatch='o', label='', width=0.8, zorder=100)
            ax.text(i+0.5, v, v, ha='center', va='bottom', fontsize=13)
        else:
            ax.bar(i, v, color='#F9E400', label='', width=0.8, zorder=100)

    ax2.plot(x, QNModel.NODE_CPA, marker='x', linestyle='-', markevery=1, markerfacecolor='none',
                    color='#7C00FE', label='')

    x_tick_label = [i+1 for i in range(QNConfig.node_num)]
    ax.set_xticks(x, x_tick_label)
    ax.tick_params(labelsize=13)
    ax.set_yticks([0,5,10,15,20,25])

    ax.set_xlabel('Topology nodes', fontsize=17)  # X轴标签
    ax.set_ylabel("Node importance", fontsize=17)  # Y轴标签
    ax2.set_ylabel("Node capacity", fontsize=17)  # Y轴标签
    ax.tick_params(axis='y', colors='k', labelsize=12)
    ax2.tick_params(axis='y', colors='#7C00FE', labelsize=12)
    # ax.grid()
    ax2.set_ylim(0, 30)

    plt.gcf().subplots_adjust(bottom=0.12)
    # plt.gcf().subplots_adjust(left=0.1, right=0.8)
    plt.grid()
    plt.show()

def draw_agent_results(agent_id):
    local_memory_usage = pd.read_csv("agent_memory_usage-5.csv")
    local_reward = pd.read_csv("agent_local_rewards--5-0.001.csv")
    x = [i for i in range(len(local_reward['0']))]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()

    agent_data = local_reward[str(agent_id)]
    avg_agent_data = take_mean_value(agent_data)
    agent_memory_data = local_memory_usage[str(agent_id)]
    avg_agent_memory_data = take_mean_value(agent_memory_data)

    # plt.plot(x, agent_data, alpha=0.3, color='#7C00FE', label='Original')
    line1, = ax.plot(x[:], avg_agent_data[:], color='#7C00FE', marker='D', markevery=400, markerfacecolor='none', label='Local rewards')
    line2, = ax2.plot(x[:], avg_agent_memory_data[:], color='#F9E400', marker='p', markevery=400, markerfacecolor='none', label='Memory usage')

    ax.xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax2.xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    ax.tick_params(labelsize=13)
    ax2.tick_params(labelsize=13)
    lines = [line1, line2]
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, fontsize=15)

    ax.set_xlabel('Episodes', fontsize=17)
    ax.set_ylabel("Local rewards", fontsize=17)
    ax2.set_ylabel("Memory usage", fontsize=17)

    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(right=0.87)
    plt.grid()
    # plt.savefig('./agent_training_results_imgs/' + str(agent_id) + "_training.png")
    plt.show()

if __name__ == '__main__':
    importance = obtain_node_importance()
    draw_node_importance(importance)
    draw_agent_results(4)
    draw_agent_results(5)
    draw_agent_results(10)