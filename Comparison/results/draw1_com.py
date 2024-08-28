import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from Config import QNConfig

def draw_colume(file_name, request_pool_len):
    x=np.arange(10)
    data = pd.read_csv(file_name)

    # plt.subplot(121)
    bar_width = 0.2
    tick_label = [(i+1)*request_pool_len for i in range(10)]
    #{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}

    plt.bar(x, [d/2 for d in data['OBO']], bar_width, color='b', hatch='o', label='OBO*50%')
    # plt.bar(x, data['OBO'], bar_width, color='b', hatch='o', label='OBO')
    plt.bar(x+bar_width, data['All_in'], bar_width, color='r', hatch='+', label='All_in')
    plt.bar(x+bar_width*2, data['SophonFixed'], bar_width, color='y', hatch='x', label='Sophon_Fixed')
    plt.bar(x+bar_width*3, data['SophonFlexible'], bar_width, color='g', hatch='*', label='Sophon_Flexible')
    plt.legend()
    plt.xticks(x+bar_width+0.05,tick_label)
    plt.gcf().subplots_adjust(bottom=0.12)

    plt.tick_params(labelsize=12)
    plt.legend(fontsize=15)  # 让图例生效
    plt.xlabel('Number of requests', fontsize=17)  # X轴标签
    plt.ylabel("Total transmission times", fontsize=17)  # Y轴标签
    plt.show()

def draw_curve(file_name, request_pool_len, arrow_pos):
    data = pd.read_csv(file_name)
    x = [(i+1)*request_pool_len for i in range(10)]

    fig, ax = plt.subplots(1, 1)

    ax.plot(x, data['OBO'], marker='o', markevery=1, color='#7C00FE', linestyle='-', markerfacecolor='none',
             label='OBO')
    ax.plot(x, data['All_in'], marker='^', markevery=1, color='#F9E400', linestyle='-.', markerfacecolor='none',
             label='All_in')
    ax.plot(x, data['SophonFixed'], marker='s', markevery=1, color='#FFAF00', linestyle='dashed', markerfacecolor='none',
             label='Sophon_Fixed')
    ax.plot(x, data['SophonFlexible'], marker='s', markevery=1, color='#F5004F', linestyle='dotted', markerfacecolor='none',
             label='Sophon_Flexible')
    fig.set_facecolor("#FFF")

    child_ax = ax.inset_axes((0.1, 0.22, 0.35, 0.35))
    child_ax.plot(x, data['OBO'], marker='o', markevery=1, color='#7C00FE', linestyle='-', markerfacecolor='none',
             label='OBO')
    child_ax.plot(x, data['SophonFlexible'], marker='s', markevery=1, color='#F5004F', linestyle='dotted', markerfacecolor='none',
             label='Sophon_Flexible')
    child_ax.set_xticks([x[i] for i in range(1, 10, 2)])
    max_child_ax_y = max(data['SophonFlexible'])
    child_ax.set_yticks([0, round(max_child_ax_y/4, 1), round(max_child_ax_y/2, 1), round(max_child_ax_y*3/4, 1), round(max_child_ax_y, 1)])
    child_ax.grid()

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Number of requests', fontsize=17)
    plt.ylabel("Algorithm execution time ($s$)", fontsize=17)
    # 添加标注
    plt.annotate(
        ' ',
        xy=(arrow_pos[0], arrow_pos[1]),
        xytext=(arrow_pos[2], arrow_pos[3]),
        arrowprops=dict(
            facecolor='black',
            shrink=0.05,
            width=1,
            alpha=0.7
        ),  # 箭头属性
        fontsize=5
    )
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    # --------draw the total transmission times------------
    # draw_colume("execute_transmission_times-5.csv", 5)
    # draw_colume("execute_transmission_times-10.csv", 10)
    # draw_colume("execute_transmission_times-15.csv", 15)
    # draw_colume("execute_transmission_times-20.csv", 20)

    # --------draw the execution time--------------------
    # draw_curve("execute_transmission_time-5.csv", 5, [25, 3, 30, 0.22])
    # draw_curve("execute_transmission_time-10.csv", 10, [50, 30, 60, 0])
    # draw_curve("execute_transmission_time-15.csv", 15, [75, 100, 100, 0])
    draw_curve("execute_transmission_time-20.csv", 20, [102, 200, 125, 0])

