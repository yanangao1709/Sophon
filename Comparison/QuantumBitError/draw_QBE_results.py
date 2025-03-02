import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

request_interval = 10

def take_average(data):
    new_data =[]
    for i, item in enumerate(data):
        if i == 0:
            new_data.append(item)
        else:
            new_data.append((sum(new_data)+item)/(i+1))
    return new_data

def draw_QBER_request():
    rel = pd.read_csv("AQBER_request.csv")
    x = [i*request_interval for i in range(len(rel['X']))]
    Two_qubit_QBER = rel['Two_qubut']
    Flexible_qubit_QBER = rel['Flexible_multi_qubit']

    plt.plot(x, Two_qubit_QBER, color='#BE2A2C', linestyle='solid', marker='o', markerfacecolor='none', markevery=10,
             label='Two-qubit QBER')
    plt.plot(x, take_average(Flexible_qubit_QBER), color='b', linestyle = 'dashed', marker='d', markerfacecolor='none', markevery=10,
             label='Multi-qubit QBER')

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Average QBER", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_SNR_request():
    rel = pd.read_csv("SNR_request.csv")
    x = [i * request_interval for i in range(len(rel['X']))]
    Two_qubit_SNR = rel['Two_qubut']
    Flexible_qubit_SNR = rel['Flexible_multi_qubit']

    plt.plot(x, Two_qubit_SNR, color='#BE2A2C', linestyle='solid', marker='o', markerfacecolor='none', markevery=10,
             label='Two-qubit SNR')
    plt.plot(x, take_average(Flexible_qubit_SNR), color='b', linestyle='dashed', marker='d', markerfacecolor='none',
             markevery=10,
             label='Multi-qubit SNR')

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Average SNR", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

def draw_QPER_request():
    rel = pd.read_csv("AQPER_request.csv")
    x = [i * request_interval for i in range(len(rel['X']))]
    Two_qubit_QPER = rel['Two_qubit']
    Flexible_qubit_QPER = rel['Flexible_multi_qubit']

    plt.plot(x, Two_qubit_QPER, color='#BE2A2C', linestyle='solid', marker='o', markerfacecolor='none', markevery=10,
             label='Two-qubit QPER')
    plt.plot(x, take_average(Flexible_qubit_QPER), color='b', linestyle='dashed', marker='d', markerfacecolor='none',
             markevery=10,
             label='Multi-qubit QPER')

    plt.tick_params(labelsize=13)
    plt.legend(fontsize=15)
    plt.xlabel('Requests', fontsize=17)
    plt.ylabel("Average QPER", fontsize=17)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    draw_QBER_request()
    draw_SNR_request()
    draw_QPER_request()

