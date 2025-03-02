import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

request_interval = 5

def draw_throughput_request_AT_fixed_topology():
    throughput_rel = pd.read_csv("Throughput_request_AT.csv")
    x = [(i+1)*request_interval for i in range(len(throughput_rel['EFiRAP']))]
    EFiRAP_throughput = throughput_rel['EFiRAP']
    Sophon_throughput = throughput_rel['Sophon']
    Multi_R_throughtput = throughput_rel['Multi-R']

    plt.plot(x, Sophon_throughput, marker='s', markevery=40, color='r', linestyle='dashed', markerfacecolor='none',
            label='Sophon_Fixed', linewidth=2)
    plt.plot(x, EFiRAP_throughput, marker='o', markevery=40, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    plt.plot(x, Multi_R_throughtput, marker='^', markevery=40, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Number of requests', fontsize=17)
    plt.ylabel("Throughput (qubits)", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_throughput_node_capacity_AT_fixed_topology():
    throughput_rel = pd.read_csv("Throughput_node_capacity_AT.csv")
    x = throughput_rel['X']
    EFiRAP_throughput = throughput_rel['EFiRAP']
    Sophon_throughput = throughput_rel['Sophon']
    Multi_R_throughtput = throughput_rel['Multi-R']

    plt.plot(x, Sophon_throughput, marker='s', markevery=1, color='r', linestyle='dashed', markerfacecolor='none',
            label='Sophon_Fixed', linewidth=2)
    plt.plot(x, EFiRAP_throughput, marker='o', markevery=1, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    plt.plot(x, Multi_R_throughtput, marker='^', markevery=1, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)

    plt.xticks([10,14,18,22,26,30])
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('The expectation of node memory', fontsize=17)
    plt.ylabel("Throughput (qubits)", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_throughput_topology_scale_AT_fixed_requests():
    throughput_rel = pd.read_csv("Throughput_topology_scale_AT.csv")
    x = [18,27,36,45,54,63,72,81,90,99,108]
    EFiRAP_throughput = throughput_rel['EFiRAP']
    Sophon_throughput = throughput_rel['Sophon']
    Multi_R_throughtput = throughput_rel['Multi-R']

    plt.plot(x, Sophon_throughput, marker='s', markevery=1, color='r', linestyle='dashed', markerfacecolor='none',
             label='Sophon_Fixed', linewidth=2)
    plt.plot(x, EFiRAP_throughput, marker='o', markevery=1, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    plt.plot(x, Multi_R_throughtput, marker='^', markevery=1, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)

    plt.xticks(x)
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Topology scale', fontsize=17)
    plt.ylabel("Throughput (qubits)", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_node_used_memory_topology_scale_AT_fixed_requests():
    throughput_rel = pd.read_csv("AMUR_topology_scale_AT.csv")
    x = [18, 27, 36, 45, 54, 63, 72, 81, 90, 99, 108]
    EFiRAP_throughput = throughput_rel['EFiRAP']
    Sophon_throughput = throughput_rel['Sophon']
    Multi_R_throughtput = throughput_rel['Multi-R']

    plt.plot(x, Sophon_throughput, marker='s', markevery=1, color='r', linestyle='dashed', markerfacecolor='none',
             label='Sophon_Fixed', linewidth=2)
    plt.plot(x, EFiRAP_throughput, marker='o', markevery=1, color='g', linestyle='-', markerfacecolor='none',
             label='EFiRAP', linewidth=2)
    plt.plot(x, Multi_R_throughtput, marker='^', markevery=1, color='y', linestyle='-.', markerfacecolor='none',
             label='Multi_R', linewidth=2)

    plt.xticks(x)
    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Topology scale', fontsize=17)
    plt.ylabel("Average memory used rate", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # draw_throughput_request_AT_fixed_topology()
    # draw_throughput_node_capacity_AT_fixed_topology()
    draw_throughput_topology_scale_AT_fixed_requests()
    draw_node_used_memory_topology_scale_AT_fixed_requests()

