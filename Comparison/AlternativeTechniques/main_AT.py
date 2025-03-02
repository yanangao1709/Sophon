import os
import pandas as pd
from copy import deepcopy
from Comparison.data.requests import *
from Topology import k_shortest_paths, RouteGenerator
from Comparison.AlternativeTechniques.EFiRAP import *
from Comparison.AlternativeTechniques.SophonFixed_AT import *
from Comparison.AlternativeTechniques.Multi_R import *
import matplotlib.pyplot as plt


def customed_weight(u, v, d):
    edge_wt = d.get("length", 1)
    return edge_wt

# use agents with |R|=5
# topology node num = 18, requiring to modify the topology scale
def baselines_one_transmission_throughput_fixed_topology():
    request_interval = 20
    EFiRAP_rel = []
    Sophon_rel = []
    Multi_rel = []
    # 固定资源内的一次传输
    for t in range(50):
        G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
        requests = ALL_REQUESTS[0:(t+1)*request_interval]
        data_volumes = DATA_VOLUMES[0:(t+1)*request_interval]
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        copy_requests = deepcopy(requests)
        copy_candidate_routes = deepcopy(candidate_routes)
        EFiRAP_throughput = EFiRAP(copy_requests, data_volumes, copy_candidate_routes)
        EFiRAP_rel.append(EFiRAP_throughput)
        # print('EFiRAP_throughput---------' + str(EFiRAP_throughput))
        Multi_R_throughput = Multi_R(copy_requests, data_volumes, copy_candidate_routes)
        Multi_rel.append(Multi_R_throughput)
        # print('Multi_R_throughput---------' + str(Multi_R_throughput))
        SophonFixed_throughput = SophonFixed(requests, data_volumes, candidate_routes, (t + 1) * request_interval)
        Sophon_rel.append(SophonFixed_throughput)
        # print('SophonFixed_throughput---------' + str(SophonFixed_throughput))
        print(t)

    x = [i for i in range(50)]
    # print(EFiRAP_rel)
    # print(Multi_rel)
    # print(Sophon_rel)
    # plt.plot(x, EFiRAP_rel, color='r')
    # plt.plot(x, Multi_rel, color='y')
    # plt.plot(x, Sophon_rel, color='b')
    # plt.show()

    throughput_rel = {}
    throughput_rel['X'] = x
    throughput_rel['EFiRAP'] = EFiRAP_rel
    throughput_rel['Multi-R'] = Multi_rel
    throughput_rel['Sophon'] = Sophon_rel
    pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\Throughput_request_AT.csv', index=False)

def baselines_node_memory_throughput_fixed_topology():
    # modify ``NODE_CPA'' in QNEnv/QNModel.py to obtain various results
    request_interval = 200

    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
    requests = ALL_REQUESTS[0:request_interval]
    data_volumes = DATA_VOLUMES[0:request_interval]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    copy_requests = deepcopy(requests)
    copy_candidate_routes = deepcopy(candidate_routes)
    EFiRAP_throughput, _ = EFiRAP(copy_requests, data_volumes, copy_candidate_routes)
    print('EFiRAP_throughput---------' + str(EFiRAP_throughput))
    Multi_R_throughput, _ = Multi_R(copy_requests, data_volumes, copy_candidate_routes)
    print('Multi_R_throughput---------' + str(Multi_R_throughput))
    SophonFixed_throughput, _ = SophonFixed(requests, data_volumes, candidate_routes, request_interval)
    print('SophonFixed_throughput---------' + str(SophonFixed_throughput))

    # ----------the exectation of NODE_CAP is 10-30, clipped by [5,35]------------
    # ----------modify ``NODE_CPA'' in QNEnv/QNModel.py to obtain different scales of node memory and record the result of each time----------
    # EFiRAP_rel = [48,42,51,49,56,62,56,75,69,69,74,76,90,93,87,100,101,107,117,116,114]
    # Multi_R_rel = [47.99999587,44.99999727,55.24999429,49.99999706,53.99999493,63.49999582,57.99999738,65.74999915,63.99999725,59.25000084,64.24999361,60.99999242,74.00000225,69.50000079,68.50000425,62.00000662,72.50000005,69.29545894,73.0000015,77.50000384,75.24999929]
    # Sophon_rel = [61,59,57,65,71,72,73,85,94,83,85,98,108,108,105,109,110,125,122,126,125]
    #
    # throughput_rel = {}
    # x = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    # throughput_rel['X'] = x
    # throughput_rel['EFiRAP'] = EFiRAP_rel
    # throughput_rel['Multi-R'] = Multi_R_rel
    # throughput_rel['Sophon'] = Sophon_rel
    # pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\Throughput_node_capacity_AT.csv', index=False)

def baselines_one_transmission_throughput_fixed_requests():
    # 1. 500 requests
    # 2. 修改不同scales的 ``Topology/topology.csv''，控制不同拓扑的读入
    # 3. 修改QNEnv下的不同scals下的QNModel
    # 4. 修改Config/TopologyConfig.py中的node_num参数
    # 5. 修改Agent加载的智能体文件路径, Provisioning/Agent.py 中的self.model.load_state_dict对应的Comparison/TrainedModel下的文件夹名
    # 6. 修改不同规模拓扑结构时，在requests.py文件中修改基于不同拓扑结构的请求集合ALL_REQUESTS

    # request_interval = 200
    # G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\..\\Topology\\topology.csv")
    # requests = ALL_REQUESTS[0:request_interval]
    # data_volumes = DATA_VOLUMES[0:request_interval]
    # # 候选路径集
    # candidate_routes = {}
    # for r_id in range(len(requests)):
    #     shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
    #                                                        QNConfig.candidate_route_num, weight=customed_weight)
    #     while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
    #         requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
    #         shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
    #                                                            QNConfig.candidate_route_num, weight=customed_weight)
    #
    #     candidate_routes[r_id] = shortest_paths[1]
    #
    # copy_requests = deepcopy(requests)
    # copy_candidate_routes = deepcopy(candidate_routes)
    # EFiRAP_throughput, EFiRAP_average_memory_used_rate = EFiRAP(copy_requests, data_volumes, copy_candidate_routes)
    # print('EFiRAP_throughput---------' + str(EFiRAP_throughput) + '-----EFiRAP_AMUR---------' + str(EFiRAP_average_memory_used_rate))
    # Multi_R_throughput, Multi_R_average_memory_used_rate = Multi_R(copy_requests, data_volumes, copy_candidate_routes)
    # print('Multi_R_throughput---------' + str(Multi_R_throughput) + '-----Multi_R_AMUR---------' + str(Multi_R_average_memory_used_rate))
    # SophonFixed_throughput, SophonFixed_average_memory_used_rate = SophonFixed(copy_requests, data_volumes, candidate_routes, request_interval)
    # print('SophonFixed_throughput---------' + str(SophonFixed_throughput) + '-----SophonFixed_AMUR---------' + str(SophonFixed_average_memory_used_rate))
    #
    # print(EFiRAP_throughput)
    # print(Multi_R_throughput)
    # print(SophonFixed_throughput)
    # print("\n")
    # print(EFiRAP_average_memory_used_rate)
    # print(Multi_R_average_memory_used_rate)
    # print(SophonFixed_average_memory_used_rate)

    # 18/27/36/45/54/63/72/81/90/108
    throughput_rel = {}
    x = [18,27,36,45,54,63,72,81,90,99,108]
    throughput_rel['X'] = x
    throughput_rel['EFiRAP'] = [60,83,77,80,104,128,117,113,135,138,138]
    throughput_rel['Multi-R'] = [57.49999473,63.50000399,76.49999844,71.99999602,95.49999909,97.00836073,110.9999952,111.5193547,122.4999926,118.3738817,131.999996]
    throughput_rel['Sophon'] = [78,92,95,102,125,130,132,142,147,155,162]
    pd.DataFrame(throughput_rel).to_csv(os.getcwd() + '\\Throughput_topology_scale_AT.csv', index=False)

    AMUR = {}
    x = [18,27,36,45,54,63,72,81,90,99,108]
    AMUR['X'] = x
    AMUR['EFiRAP'] = [0.4389318,0.409385894,0.356525889,0.307293872,0.315891002,0.33320745,0.326909144,0.285825022,0.311198223,0.28596172,0.28836609]
    AMUR['Multi-R'] = [0.386710771,0.298122051,0.305483848,0.222026571,0.255880924,0.251307696,0.253951031,0.189106093,0.23520732,0.174046678,0.195870825]
    AMUR['Sophon'] = [0.603380481,0.486308405,0.478726568,0.444954429,0.407453918,0.388509322,0.397102488,0.382346986,0.377108288,0.378896705,0.380634774]
    pd.DataFrame(AMUR).to_csv(os.getcwd() + '\\AMUR_topology_scale_AT.csv', index=False)



if __name__ == '__main__':
    # -------------------one-time-transmission-throughput with fixed topology (18) and changeable requests---------
    # baselines_one_transmission_throughput_fixed_topology()
    # -------------------fixed topology (18) and fixed requests (200)----------------------
    # baselines_node_memory_throughput_fixed_topology()

    # -------------------one-time-transmission-throughput with fixed requests 1000 and changeable topology----------
    baselines_one_transmission_throughput_fixed_requests()


