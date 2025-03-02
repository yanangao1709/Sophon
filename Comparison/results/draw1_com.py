import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from Config import QNConfig

def take_average(data):
    new_data =[]
    for i, item in enumerate(data):
        if i == 0:
            new_data.append(item)
        else:
            new_data.append((sum(new_data)+item)/(i+1))
    return new_data

def draw_colume():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\communication_cost.csv")
    x = np.arange(len(data['EFiRAP']))

    bar_width = 0.2
    tick_label = [(i+1)*QNConfig.request_pool_len for i in range(len(data['EFiRAP']))]
    #{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}

    plt.bar(x, [d for d in data['EFiRAP']], bar_width, color='b', hatch='o', label='EFiRAP')
    plt.bar(x+bar_width, data['Multi_R'], bar_width, color='r', hatch='+', label='Multi_R')
    plt.bar(x+bar_width*2, data['SophonFixed'], bar_width, color='y', hatch='x', label='Sophon_Fixed')
    plt.bar(x+bar_width*3, data['SophonFlexible'], bar_width, color='g', hatch='*', label='Sophon_Flexible')
    plt.legend()
    plt.xticks(x+bar_width+0.05,tick_label)
    plt.gcf().subplots_adjust(bottom=0.12)

    plt.tick_params(labelsize=12)
    plt.legend(fontsize=15)  # 让图例生效
    plt.xlabel('Number of requests', fontsize=17)  # X轴标签
    plt.ylabel("The communication cost", fontsize=17)  # Y轴标签
    plt.show()

def draw_curve_with_subfig():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\algorithm_exe_time.csv")
    x = [(i + 1) * QNConfig.request_pool_len for i in range(len(data['EFiRAP']))]

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['EFiRAP'], marker='o', markevery=2, color='g', linestyle='-', markerfacecolor='none',
            label='EFiRAP')
    ax.plot(x, data['Multi_R'], marker='^', markevery=2, color='y', linestyle='-.', markerfacecolor='none',
            label='Multi_R')
    ax.plot(x, take_average(data['SophonFixed']), marker='s', markevery=2, color='r', linestyle='dashed',
            markerfacecolor='none',
            label='Sophon_Fixed')
    ax.plot(x, data['SophonFlexible'], marker='*', markevery=2, color='b', linestyle='dotted', markerfacecolor='none',
            label='Sophon_Flexible')
    fig.set_facecolor("#FFF")

    child_ax = ax.inset_axes((0.1, 0.22, 0.35, 0.35))
    child_ax.plot(x, data['EFiRAP'], marker='o', markevery=1, color='#7C00FE', linestyle='-', markerfacecolor='none',
             label='EFiRAP')
    child_ax.plot(x, data['SophonFlexible'], marker='s', markevery=1, color='#F5004F', linestyle='dotted', markerfacecolor='none',
             label='Sophon_Flexible')
    child_ax.set_xticks([x[i] for i in range(1, 10, 2)])
    max_child_ax_y = max(data['SophonFlexible'])
    child_ax.set_yticks([0, round(max_child_ax_y/4, 1), round(max_child_ax_y/2, 1), round(max_child_ax_y*3/4, 1), round(max_child_ax_y, 1)])
    child_ax.grid()

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Number of requests', fontsize=17)
    plt.ylabel("The algorithm running time", fontsize=17)
    # 添加标注
    # plt.annotate(
    #     ' ',
    #     xy=(arrow_pos[0], arrow_pos[1]),
    #     xytext=(arrow_pos[2], arrow_pos[3]),
    #     arrowprops=dict(
    #         facecolor='black',
    #         shrink=0.05,
    #         width=1,
    #         alpha=0.7
    #     ),  # 箭头属性
    #     fontsize=5
    # )
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_curve_cc():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\communication_cost--.csv")
    x = [(i+1)*QNConfig.request_pool_len for i in range(len(data['EFiRAP']))]
    # data2 = data.copy()
    # data2["Multi_R"] = data['EFiRAP']
    # data2["EFiRAP"] = data['Multi_R']
    # pd.DataFrame(data2).to_csv('D:\\Python\\Sophon\\Comparison\\results\\communication_cost--.csv', index=False)

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['EFiRAP'], marker='o', markevery=2, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    ax.plot(x, data['Multi_R'], marker='^', markevery=2, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)
    ax.plot(x, data['SophonFixed'], marker='s', markevery=2, color='r', linestyle='dashed', markerfacecolor='none',
             label='Sophon_Fixed', linewidth=2)
    ax.plot(x, data['SophonFlexible'], marker='*', markevery=2, color='b', linestyle='dotted', markerfacecolor='none',
             label='Sophon_Flexible', linewidth=2)
    fig.set_facecolor("#FFF")

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Number of requests', fontsize=17)
    plt.ylabel("The communication cost", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_curve_et():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\algorithm_exe_time.csv")
    x = [(i+1)*QNConfig.request_pool_len for i in range(len(data['EFiRAP']))]

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['EFiRAP'], marker='o', markevery=3, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    ax.plot(x, data['Multi_R'], marker='^', markevery=3, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)
    ax.plot(x, take_average(data['SophonFixed']), marker='s', markevery=3, color='r', linestyle='dashed', markerfacecolor='none',
             label='Sophon_Fixed', linewidth=2)
    ax.plot(x, data['SophonFlexible'], marker='*', markevery=3, color='b', linestyle='dotted', markerfacecolor='none',
             label='Sophon_Flexible', linewidth=2)
    fig.set_facecolor("#FFF")

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Number of requests', fontsize=17)
    plt.ylabel("The algorithm running time", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_curve_cc_fixed_requests():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\communication_cost_fixed_requests.csv")
    x = [18,27,36,45,54,63,72,81,90,99,108]

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['EFiRAP'], marker='o', markevery=1, color='g', linestyle='-', markerfacecolor='none',
            label='EFiRAP', linewidth=2)
    ax.plot(x, data['Multi_R'], marker='^', markevery=1, color='y', linestyle='-.', markerfacecolor='none',
            label='Multi_R', linewidth=2)
    ax.plot(x, data['SophonFixed'], marker='s', markevery=1, color='r', linestyle='dashed', markerfacecolor='none',
            label='Sophon_Fixed', linewidth=2)
    ax.plot(x, data['SophonFlexible'], marker='*', markevery=1, color='b', linestyle='dotted', markerfacecolor='none',
            label='Sophon_Flexible', linewidth=2)
    fig.set_facecolor("#FFF")

    plt.xticks(x)
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Topology scale', fontsize=17)
    plt.ylabel("The communication cost", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_curve_et_fixed_requests():
    data = pd.read_csv("D:\\Python\\Sophon\\Comparison\\results\\algorithm_exe_time_fixed_requests.csv")
    x = [18,27,36,45,54,63,72,81,90,99,108]

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['EFiRAP'], marker='o', markevery=1, color='g', linestyle='-', markerfacecolor='none',
            label='EFiRAP', linewidth=2)
    ax.plot(x, data['Multi_R'], marker='^', markevery=1, color='y', linestyle='-.', markerfacecolor='none',
            label='Multi_R', linewidth=2)
    ax.plot(x, take_average(data['SophonFixed']), marker='s', markevery=1, color='r', linestyle='dashed',
            markerfacecolor='none',
            label='Sophon_Fixed', linewidth=2)
    ax.plot(x, data['SophonFlexible'], marker='*', markevery=1, color='b', linestyle='dotted', markerfacecolor='none',
            label='Sophon_Flexible', linewidth=2)
    fig.set_facecolor("#FFF")

    plt.xticks(x)
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Topology scale', fontsize=17)
    plt.ylabel("The algorithm running time", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()


def draw_curve_communication_threshold():
    rel_18 = pd.read_csv("adjust_threshold_communication_18.csv")
    rel_27 = pd.read_csv("adjust_threshold_communication_27.csv")
    rel_36 = pd.read_csv("adjust_threshold_communication_36.csv")
    rel_45 = pd.read_csv("adjust_threshold_communication_45.csv")
    x = [i for i in range(len(rel_18['communication_threshold']))]
    comleted_request_number_18 = rel_18['completed_request_num']
    comleted_request_number_27 = rel_27['completed_request_num']
    comleted_request_number_36 = rel_36['completed_request_num']
    comleted_request_number_45 = rel_45['completed_request_num']

    plt.plot(x, comleted_request_number_18, color='#BE2A2C', linestyle='solid', marker='o', markerfacecolor='none',
             markevery=10,
             label='18-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_27, color='b', linestyle='solid', marker='^', markerfacecolor='none',
             markevery=10,
             label='27-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_36, color='y', linestyle='solid', marker='*', markerfacecolor='none',
             markevery=10,
             label='36-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_45, color='g', linestyle='solid', marker='s', markerfacecolor='none',
             markevery=10,
             label='45-node topology', linewidth=2)

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Communication cost thresholds', fontsize=17)
    plt.ylabel("Number of completed requests", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_curve_computing_threshold():
    rel_18 = pd.read_csv("adjust_threshold_computing_18.csv")
    rel_27 = pd.read_csv("adjust_threshold_computing_27.csv")
    rel_36 = pd.read_csv("adjust_threshold_computing_36.csv")
    rel_45 = pd.read_csv("adjust_threshold_computing_45.csv")
    x = [i for i in range(len(rel_18['communication_threshold']))]
    comleted_request_number_18 = rel_18['completed_request_num']
    comleted_request_number_27 = rel_27['completed_request_num']
    comleted_request_number_36 = rel_36['completed_request_num']
    comleted_request_number_45 = rel_45['completed_request_num']

    plt.plot(x, comleted_request_number_18, color='#BE2A2C', linestyle='solid', marker='o', markerfacecolor='none',
             markevery=10,
             label='18-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_27, color='b', linestyle='solid', marker='^', markerfacecolor='none',
             markevery=10,
             label='27-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_36, color='y', linestyle='solid', marker='*', markerfacecolor='none',
             markevery=10,
             label='36-node topology', linewidth=2)
    plt.plot(x, comleted_request_number_45, color='g', linestyle='solid', marker='s', markerfacecolor='none',
             markevery=10,
             label='45-node topology', linewidth=2)

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Algorithm running time (ms)', fontsize=17)
    plt.ylabel("Number of completed requests", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    # # --------draw the communication cost with a fixed topology---------------
    draw_curve_cc()
    #
    # # --------draw the algorithm execution time with a fixed topology---------
    draw_curve_et()

    # # --------draw the communication cost with a fixed requests------------
    draw_curve_cc_fixed_requests()
    # # --------draw the algorithm execution time with fixed requests---------
    draw_curve_et_fixed_requests()

    # --------draw the communication thresholds--------------------
    # draw_curve_communication_threshold()
    # draw_curve_computing_threshold()

