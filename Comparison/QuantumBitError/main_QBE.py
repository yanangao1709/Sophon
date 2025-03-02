import os
import pandas as pd
from copy import deepcopy
from Comparison.data.requests import *
from Topology import k_shortest_paths, RouteGenerator
from Comparison.QuantumBitError.SophonFixed_QBER import *


def customed_weight(u, v, d):
    edge_wt = d.get("length", 1)
    return edge_wt

# use agents with |R|=5
# topology node num = 18, requiring to modify the topology scale
def Average_QBER():
    request_interval = 10
    Sophon_rel = []
    Flexible_AQBER = []
    # 固定资源内的一次传输
    for t in range(100):
        G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
        requests = ALL_REQUESTS[0:(t+1)*request_interval]
        data_volumes = DATA_VOLUMES[0:(t+1)*request_interval]
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
            while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
                requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
                shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                                   QNConfig.candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        copy_requests = deepcopy(requests)
        copy_candidate_routes = deepcopy(candidate_routes)
        two_qubit_AQBER = SophonFixed_QBER_2(copy_requests, data_volumes, copy_candidate_routes, (t + 1) * request_interval)
        Sophon_rel.append(two_qubit_AQBER)
        print('SophonFixed_two_qubit_QBER---------' + str(two_qubit_AQBER))
        Flexible_Sophon_ABER = SophonFixed_QBER_flexible(copy_requests, data_volumes, copy_candidate_routes, (t + 1) * request_interval)
        Flexible_AQBER.append(Flexible_Sophon_ABER)
        print('SophonFixed_multi_qubit_QBER---------' + str(Flexible_Sophon_ABER))
        print(t)

    x = [i for i in range(100)]
    # print(EFiRAP_rel)
    # print(Multi_rel)
    # print(Sophon_rel)
    # plt.plot(x, EFiRAP_rel, color='r')
    # plt.plot(x, Multi_rel, color='y')
    # plt.plot(x, Sophon_rel, color='b')
    # plt.show()

    throughput_rel = {}
    throughput_rel['X'] = x
    throughput_rel['Two_qubut'] = Sophon_rel
    throughput_rel['Flexible_multi_qubit'] = Flexible_AQBER
    pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\AQBER_request.csv', index=False)

def Average_SNR():
    request_interval = 10
    Sophon_rel = []
    Flexible_SNR = []
    # 固定资源内的一次传输
    for t in range(100):
        G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
        requests = ALL_REQUESTS[0:(t + 1) * request_interval]
        data_volumes = DATA_VOLUMES[0:(t + 1) * request_interval]
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
            while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
                requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
                shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                                   QNConfig.candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        copy_requests = deepcopy(requests)
        copy_candidate_routes = deepcopy(candidate_routes)
        two_qubit_average_route_SNR = SophonFixed_SNR_2(copy_requests, data_volumes, copy_candidate_routes,
                                             (t + 1) * request_interval)
        Sophon_rel.append(two_qubit_average_route_SNR)
        print('SophonFixed_two_qubit_SNR---------' + str(two_qubit_average_route_SNR))
        Flexible_average_route_SNR = SophonFixed_SNR_flexible(copy_requests, data_volumes, copy_candidate_routes,
                                                         (t + 1) * request_interval)
        Flexible_SNR.append(Flexible_average_route_SNR)
        print('SophonFixed_multi_qubit_SNR---------' + str(Flexible_average_route_SNR))
        print(t)

    x = [i for i in range(100)]
    # print(EFiRAP_rel)
    # print(Multi_rel)
    # print(Sophon_rel)
    # plt.plot(x, EFiRAP_rel, color='r')
    # plt.plot(x, Multi_rel, color='y')
    # plt.plot(x, Sophon_rel, color='b')
    # plt.show()

    throughput_rel = {}
    throughput_rel['X'] = x
    throughput_rel['Two_qubut'] = Sophon_rel
    throughput_rel['Flexible_multi_qubit'] = Flexible_SNR
    pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\SNR_request.csv', index=False)

def Average_QPER():
    request_interval = 10
    Sophon_rel = []
    Flexible_AQPER = []
    # 固定资源内的一次传输
    for t in range(100):
        G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
        requests = ALL_REQUESTS[0:(t + 1) * request_interval]
        data_volumes = DATA_VOLUMES[0:(t + 1) * request_interval]
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
            while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
                requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
                shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                                   QNConfig.candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        copy_requests = deepcopy(requests)
        copy_candidate_routes = deepcopy(candidate_routes)
        two_qubit_AQPER = SophonFixed_QPER_2(copy_requests, data_volumes, copy_candidate_routes,
                                             (t + 1) * request_interval)
        Sophon_rel.append(two_qubit_AQPER)
        print('SophonFixed_two_qubit_QBER---------' + str(two_qubit_AQPER))
        Flexible_Sophon_AQPER = SophonFixed_QPER_flexible(copy_requests, data_volumes, copy_candidate_routes,
                                                         (t + 1) * request_interval)
        Flexible_AQPER.append(Flexible_Sophon_AQPER)
        print('SophonFixed_multi_qubit_QBER---------' + str(Flexible_Sophon_AQPER))
        print(t)

    x = [i for i in range(100)]
    # print(EFiRAP_rel)
    # print(Multi_rel)
    # print(Sophon_rel)
    # plt.plot(x, EFiRAP_rel, color='r')
    # plt.plot(x, Multi_rel, color='y')
    # plt.plot(x, Sophon_rel, color='b')
    # plt.show()

    throughput_rel = {}
    throughput_rel['X'] = x
    throughput_rel['Two_qubit'] = Sophon_rel
    throughput_rel['Flexible_multi_qubit'] = Flexible_AQPER
    pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\AQPER_request.csv', index=False)

if __name__ == '__main__':
    Average_QBER()
    Average_SNR()
    Average_QPER()


