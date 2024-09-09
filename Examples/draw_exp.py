import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import mpl_toolkits.axisartist as axisartist


def draw_1():
    x = [0,1,2,3,4,5,6]
    # 所有请求所需传输的数据量为10
    y_OBO = [0, 5, 10, 15, 20, 25, 30]
    y_AI = [0, 5, 10, 10, 13, 15, 18]
    y_AMOR = [0, 5, 10, 11, 13, 13, 15]

    fig = plt.figure()
    # -------------对于前两个绘制的阴影处理--------
    y_err = 5   # 10所需阴影处理
    max_val = max(y_OBO)
    y_upper1 = [min(max_val, i+y_err) for i in y_OBO]
    y_lower1 = [max(0, i-y_err) for i in y_OBO]
    y_upper2 = [min(max_val, i+y_err) for i in y_AI]
    y_lower2 = [max(0, i-y_err) for i in y_AI]
    y_upper3 = [min(max_val, i+y_err) for i in y_AMOR]
    y_lower3 = [max(0, i-y_err) for i in y_AMOR]

    plt.plot(x, y_OBO, alpha=0.5, color='g', marker='s', markevery=1, label='OBO')
    plt.plot(x, y_AI, alpha=0.5, color='b', marker='^', markevery=1, label='All_in')
    plt.plot(x, y_AMOR, alpha=0.5, color='r', marker='o', markevery=1, label='AMOR')
    plt.fill_between(x, y_lower1, y_upper1, color='g', alpha=0.1)
    plt.fill_between(x, y_lower2, y_upper2, color='b', alpha=0.1)
    plt.fill_between(x, y_lower3, y_upper3, color='r', alpha=0.1)
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=17)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Transmitting times", fontsize=20)

    # 添加标注
    plt.annotate(
        'Start competing for resources',  # 标注文本
        xy=(2,9),  # 标注点位置 (2,9)\(2,98)\(2,80)
        xytext=(2,2),  # 标注文本位置 (2,2)\(2,20)\(2,20)
        arrowprops=dict(
            facecolor='black',
            shrink=0.1,
            width=1,
            alpha=0.7
        ),  # 箭头属性
        fontsize=15
    )
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(left=0.14)
    # plt.grid()
    plt.show()

def draw_2():
    x = [0, 1, 2, 3, 4, 5, 6]

    # 所有请求所需传输的数据量为100
    y_OBO = [0, 50, 100, 150, 200, 250, 300]
    y_AI = [0, 50, 100, 100, 125, 150, 175]
    y_AMOR = [0, 50, 100, 100, 125, 125, 150]

    fig = plt.figure()
    # -------------对于前两个绘制的阴影处理--------
    y_err= 50   # 100所需阴影处理
    max_val = max(y_OBO)
    y_upper1 = [min(max_val, i+y_err) for i in y_OBO]
    y_lower1 = [max(0, i-y_err) for i in y_OBO]
    y_upper2 = [min(max_val, i+y_err) for i in y_AI]
    y_lower2 = [max(0, i-y_err) for i in y_AI]
    y_upper3 = [min(max_val, i+y_err) for i in y_AMOR]
    y_lower3 = [max(0, i-y_err) for i in y_AMOR]

    plt.plot(x, y_OBO, alpha=0.5, color='g', marker='s', markevery=1, label='OBO')
    plt.plot(x, y_AI, alpha=0.5, color='b', marker='^', markevery=1, label='All_in')
    plt.plot(x, y_AMOR, alpha=0.5, color='r', marker='o', markevery=1, label='AMOR')
    plt.fill_between(x, y_lower1, y_upper1, color='g', alpha=0.1)
    plt.fill_between(x, y_lower2, y_upper2, color='b', alpha=0.1)
    plt.fill_between(x, y_lower3, y_upper3, color='r', alpha=0.1)
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=17)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Transmitting times", fontsize=20)

    # 添加标注
    plt.annotate(
        'Start competing for resources',  # 标注文本
        xy=(2,98),  # 标注点位置 (2,9)\(2,98)\(2,80)
        xytext=(2,20),  # 标注文本位置 (2,2)\(2,20)\(2,20)
        arrowprops=dict(
            facecolor='black',
            shrink=0.1,
            width=1,
            alpha=0.7
        ),  # 箭头属性
        fontsize=15
    )
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(left=0.14)
    # plt.grid()
    plt.show()

def draw_3():
    x = [0, 1, 2, 3, 4, 5, 6]

    # 所有请求所需传输的数据量为[128,40,10,96,189,57]
    y_OBO = [0, 64, 84, 89, 137, 232, 261]
    y_AI = [0, 64, 84, 84, 102, 115, 139]
    y_AMOR = [0, 64, 84, 85, 84, 106, 131]

    fig = plt.figure()
    # -------------对于第三个绘制的阴影处理---------
    y_err = 50  # 不均匀数据请求所需阴影处理
    max_val = max(y_OBO)
    y_upper1 = [i + y_err for i in y_OBO]
    y_lower1 = [i - y_err for i in y_OBO]
    y_upper2 = [i + y_err for i in y_AI]
    y_lower2 = [i - y_err for i in y_AI]
    y_upper3 = [i + y_err for i in y_AMOR]
    y_lower3 = [i - y_err for i in y_AMOR]
    y_lower1[0] = 0
    y_lower2[0] = 0
    y_lower3[0] = 0
    y_lower1[1] = 0
    y_lower2[1] = 0
    y_lower3[1] = 0
    y_upper1[-1] = max_val

    plt.plot(x, y_OBO, alpha=0.5, color='g', marker='s', markevery=1, label='OBO')
    plt.plot(x, y_AI, alpha=0.5, color='b', marker='^', markevery=1, label='All_in')
    plt.plot(x, y_AMOR, alpha=0.5, color='r', marker='o', markevery=1, label='AMOR')
    plt.fill_between(x, y_lower1, y_upper1, color='g', alpha=0.1)
    plt.fill_between(x, y_lower2, y_upper2, color='b', alpha=0.1)
    plt.fill_between(x, y_lower3, y_upper3, color='r', alpha=0.1)
    # plt.gca().yaxis.set_major_formatter(mtick.ScalarFormatter(useMathText = True))
    # plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=17)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Transmitting times", fontsize=20)

    # 添加标注
    plt.annotate(
        'Start competing for resources',  # 标注文本
        xy=(2, 80),  # 标注点位置 (2,9)\(2,98)\(2,80)
        xytext=(2, 20),  # 标注文本位置 (2,2)\(2,20)\(2,20)
        arrowprops=dict(
            facecolor='black',
            shrink=0.1,
            width=1,
            alpha=0.7
        ),  # 箭头属性
        fontsize=15
    )
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.gcf().subplots_adjust(left=0.14)
    # plt.grid()
    plt.show()


if __name__ == '__main__':
    # draw_1()
    # draw_2()
    draw_3()
