# -------------------------Figure 12----------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Config import QNConfig
from QNEnv import QNModel
import matplotlib.ticker as mtick
import random
from Topology import RouteGenerator

def draw_heterogeneous_requsts_mu():
    data_mu = pd.read_csv("..\\Comparison\\results\\heterogeneous_requests_mu.csv")
    x = data_mu['mu']

    # plt.subplot(121)
    bar_width = 0.4
    tick_label = [10+(i + 1) for i in range(5)]
    # {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}

    plt.bar(x, data_mu['SophonFixed'], bar_width, color='b', hatch='o', label='Sophon_Fixed')
    plt.bar(x + bar_width, data_mu['SophonFlexible'], bar_width, color='r', hatch='+', label='Sophon_Flexible')

    plt.legend()
    plt.xticks(x+0.08, tick_label)

    plt.tick_params(labelsize=12)
    plt.legend(fontsize=15)  # 让图例生效
    plt.xlabel('Expectation $\mu$', fontsize=17)  # X轴标签
    plt.ylabel("Total transmission times", fontsize=17)  # Y轴标签
    plt.gcf().subplots_adjust(bottom=0.13)
    plt.grid()
    plt.show()

def draw_heterogeneous_requsts_sigma():
    data_sigma = pd.read_csv("..\\Comparison\\results\\heterogeneous_requests_sigma.csv")
    x = data_sigma['sigma']

    # plt.subplot(121)
    bar_width = 0.12
    tick_label = [round(0.3 * (i + 1), 1) for i in range(5)]
    # {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}

    plt.bar(x, data_sigma['SophonFixed'], bar_width, color='b', hatch='o', label='Sophon_Fixed')
    plt.bar(x + bar_width, data_sigma['SophonFlexible'], bar_width, color='r', hatch='+', label='Sophon_Flexible')

    plt.legend()
    plt.xticks(x+0.06, tick_label)

    plt.tick_params(labelsize=12)
    plt.legend(fontsize=15)  # 让图例生效
    plt.xlabel('Variance $\sigma$', fontsize=17)  # X轴标签
    plt.ylabel("Total transmission times", fontsize=17)  # Y轴标签
    plt.gcf().subplots_adjust(bottom=0.13)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    draw_heterogeneous_requsts_mu()
    draw_heterogeneous_requsts_sigma()