#  当测试部署模式为Fixed requests， 修改相应请求生成接口

from Comparison.data.requests import *
from Topology import k_shortest_paths, RouteGenerator
import pandas as pd
from Comparison.EFiRAP_com import *
from Comparison.Multi_R_com import *
from Comparison.SophonFixed_com import *
from Comparison.SophonFlexible_com import *
import numpy as np

def customed_weight(u, v, d):
    edge_wt = d.get("length", 1)
    return edge_wt

def baseline_comparison_fixed_topology():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    EFiRAP_cc = []
    Multi_R_cc = []
    Sophon_Fixed_cc = []
    Sophon_Flexible_cc = []

    EFiRAP_et = []
    Multi_R_et = []
    Sophon_Fixed_et = []
    Sophon_Flexible_et = []

    for time in range(100):
        print(time)
        requests = ALL_REQUESTS[0:(time+1)*QNConfig.request_pool_len]
        data_volumes = DATA_VOLUMES[0:(time+1)*QNConfig.request_pool_len]

        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
            while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
                requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
                shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                                   QNConfig.candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        EFiRAP_cc_rel = EFiRAP_com(requests, data_volumes, candidate_routes)
        time_EFiRAP_one_time = EFiRAP_time(requests, data_volumes, candidate_routes)
        EFiRAP_cc.append(EFiRAP_cc_rel)
        EFiRAP_et.append(time_EFiRAP_one_time)
        print("EFiRAP_communication_cost:" + str(EFiRAP_cc_rel) + "------" + "EFiRAP_algorithm_exe_time:" +
              str(time_EFiRAP_one_time/len(requests)))

        Multi_R_cc_rel = Multi_R_com(requests, data_volumes, candidate_routes)
        time_Multi_R_one_time = Multi_R_time(requests, data_volumes, candidate_routes)
        Multi_R_cc.append(Multi_R_cc_rel)
        Multi_R_et.append(time_Multi_R_one_time)
        print("Multi_R_communication_cost:" + str(Multi_R_cc_rel) + "------" + "Multi_R_algorithm_exe_time:" + str(
            time_Multi_R_one_time))

        SophonFixed_cc_rel = SophonFixed(requests, data_volumes, candidate_routes, (time+1)*QNConfig.request_pool_len)
        time_SophonFixed_one_time = SophonFixed_time(requests, data_volumes, candidate_routes, (time+1)*QNConfig.request_pool_len)
        Sophon_Fixed_cc.append(SophonFixed_cc_rel)
        Sophon_Fixed_et.append(time_SophonFixed_one_time)
        print("Sophon_Fixed_communication_cost:" + str(SophonFixed_cc_rel) + "------" + "Sophon_Fixed_algorithm_exe_time:" + str(
            time_SophonFixed_one_time/len(requests)))

        Sophon_Flexible_cc_rel = SophonFlexible((time+1)*QNConfig.request_pool_len)
        time_Sophon_Flexible_one_time = SophonFlexible_time((time+1)*QNConfig.request_pool_len)
        Sophon_Flexible_cc.append(Sophon_Flexible_cc_rel)
        Sophon_Flexible_et.append(time_Sophon_Flexible_one_time)
        print("Sophon_Flexible_communication_cost:" + str(
            Sophon_Flexible_cc_rel) + "------" + "Sophon_Flexible_algorithm_exe_time:" + str(
            time_Sophon_Flexible_one_time/len(requests)))

    COM_COST = {}
    COM_COST["EFiRAP"] = EFiRAP_cc
    COM_COST["Multi_R"] = Multi_R_cc
    COM_COST["SophonFixed"] = Sophon_Fixed_cc
    COM_COST["SophonFlexible"] = Sophon_Flexible_cc
    pd.DataFrame(COM_COST).to_csv('D:\\Python\\Sophon\\Comparison\\results\\communication_cost.csv', index=False)

    EXE_TIME = {}
    EXE_TIME['EFiRAP'] = EFiRAP_et
    EXE_TIME['Multi_R'] = Multi_R_et
    EXE_TIME['SophonFixed'] = Sophon_Fixed_et
    EXE_TIME['SophonFlexible'] = Sophon_Flexible_et
    pd.DataFrame(EXE_TIME).to_csv('D:\\Python\\Sophon\\Comparison\\results\\algorithm_exe_time.csv', index=False)

def baseline_comparison_fixed_request():
    # G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")
    #
    # request_num = 200
    # requests = ALL_REQUESTS[0:request_num]
    # data_volumes = DATA_VOLUMES[0:request_num]
    #
    # candidate_routes = {}
    # for r_id in range(len(requests)):
    #     shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
    #                                                        QNConfig.candidate_route_num, weight=customed_weight)
    #     while (shortest_paths == None) or (len(shortest_paths[1]) != QNConfig.candidate_route_num):
    #         requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
    #         shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
    #                                                            QNConfig.candidate_route_num, weight=customed_weight)
    #     candidate_routes[r_id] = shortest_paths[1]
    #
    # EFiRAP_cc_rel = EFiRAP_com(requests, data_volumes, candidate_routes)
    # time_EFiRAP_one_time = EFiRAP_time(requests, data_volumes, candidate_routes)
    # print("EFiRAP_communication_cost:" + str(EFiRAP_cc_rel) + "------" + "EFiRAP_algorithm_exe_time:" +
    #       str(time_EFiRAP_one_time / len(requests)))
    #
    # Multi_R_cc_rel = Multi_R_com(requests, data_volumes, candidate_routes)
    # time_Multi_R_one_time = Multi_R_time(requests, data_volumes, candidate_routes)
    # print("Multi_R_communication_cost:" + str(Multi_R_cc_rel) + "------" + "Multi_R_algorithm_exe_time:" + str(
    #     time_Multi_R_one_time))
    #
    # SophonFixed_cc_rel = SophonFixed(requests, data_volumes, candidate_routes,
    #                                  request_num)
    # time_SophonFixed_one_time = SophonFixed_time(requests, data_volumes, candidate_routes,
    #                                              request_num)
    # print("Sophon_Fixed_communication_cost:" + str(
    #     SophonFixed_cc_rel) + "------" + "Sophon_Fixed_algorithm_exe_time:" + str(
    #     time_SophonFixed_one_time / len(requests)))
    #
    # Sophon_Flexible_cc_rel = SophonFlexible(request_num)
    # time_Sophon_Flexible_one_time = SophonFlexible_time(request_num)
    # print("Sophon_Flexible_communication_cost:" + str(
    #     Sophon_Flexible_cc_rel) + "------" + "Sophon_Flexible_algorithm_exe_time:" + str(
    #     time_Sophon_Flexible_one_time / len(requests)))
    #
    # print(EFiRAP_cc_rel)
    # print(Multi_R_cc_rel)
    # print(SophonFixed_cc_rel)
    # print(Sophon_Flexible_cc_rel)
    # print("\n")
    # print(time_EFiRAP_one_time)
    # print(time_Multi_R_one_time)
    # print(time_SophonFixed_one_time)
    # print(time_Sophon_Flexible_one_time)

    # 18/27/36/45/54/63/72/81/90/108
    EFiRAP_cc = [100,101,99,106,90,97,91,92,97,88,77]
    Multi_R_cc = [95,80,99,77,82,58,82,68,93,65,73]
    Sophon_Fixed_cc = [43, 44, 41, 49, 38, 37, 40, 38, 35, 35, 37]
    Sophon_Flexible_cc = [84,52,62,73,60,39,56,48,55,44,48]

    EFiRAP_et = [0.584849834,0.603558064,0.624624014,0.639189005,0.658952951,0.685281038,0.696619987,0.72601819,0.743093014,0.756181002,0.77306819]
    Multi_R_et = [0.212852275,0.249839573,0.260043271,0.294374526,0.3157273,0.320013225,0.362494853,0.409092023,0.445044473,0.465638055,0.510233827]
    Sophon_Fixed_et = [0.045573015,0.034999886,0.055096912,0.07994184,0.097007799,0.127037096,0.158001947,0.237999964,0.254507837,0.289051104,0.377029982]
    Sophon_Flexible_et = [0.010999918,0.012028933,0.015031099,0.021031141,0.025969982,0.029996872,0.036999941,0.042999983,0.044000864,0.05203104,0.055032015]

    COM_COST = {}
    COM_COST["EFiRAP"] = EFiRAP_cc
    COM_COST["Multi_R"] = Multi_R_cc
    COM_COST["SophonFixed"] = Sophon_Fixed_cc
    COM_COST["SophonFlexible"] = Sophon_Flexible_cc
    pd.DataFrame(COM_COST).to_csv('D:\\Python\\Sophon\\Comparison\\results\\communication_cost_fixed_requests.csv', index=False)

    EXE_TIME = {}
    EXE_TIME['EFiRAP'] = EFiRAP_et
    EXE_TIME['Multi_R'] = Multi_R_et
    EXE_TIME['SophonFixed'] = Sophon_Fixed_et
    EXE_TIME['SophonFlexible'] = Sophon_Flexible_et
    pd.DataFrame(EXE_TIME).to_csv('D:\\Python\\Sophon\\Comparison\\results\\algorithm_exe_time_fixed_requests.csv', index=False)


def generate_gaussian_random_numbers(mu, sigma, completed_requests_num, min_value=10, max_value=20):
    assert sigma * 3 < (max_value - min_value) / 2
    random_numbers = np.random.normal(mu, sigma, completed_requests_num)
    result = np.clip(random_numbers, min_value, max_value)
    results = []
    for r in result:
        results.append(int(r))
    return results

def heterogeneous_requests_mu():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 20
    requests = ALL_REQUESTS[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    heterogeneous_requests_results = {}
    Sophon_Fixed = []
    Sophon_Flexible = []
    mu_s = []
    sigma = 1
    for mu in range(5):
        new_data_volumes = generate_gaussian_random_numbers(10+(mu+1)*1, sigma, completed_requests_num)
        Sophon_rel_Fixed = SophonFixed(requests, new_data_volumes, candidate_routes, completed_requests_num)
        Sophon_rel_Flexible = SophonFlexible(completed_requests_num, 10+(mu+1)*1, sigma, True)
        mu_s.append(10+(mu+1)*1)
        Sophon_Fixed.append(Sophon_rel_Fixed)
        Sophon_Flexible.append(Sophon_rel_Flexible)
    print(Sophon_Fixed)
    print(Sophon_Flexible)

    heterogeneous_requests_results['mu'] = mu_s
    heterogeneous_requests_results['SophonFixed'] = Sophon_Fixed
    heterogeneous_requests_results['SophonFlexible'] = Sophon_Flexible
    pd.DataFrame(heterogeneous_requests_results).to_csv(os.getcwd() + '\\..\\Comparison\\results\\heterogeneous_requests_mu.csv', index=False)

def heterogeneous_requests_sigma():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 20
    requests = ALL_REQUESTS[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    heterogeneous_requests_results = {}
    Sophon_Fixed = []
    Sophon_Flexible = []
    mu = 15
    sigma_s = []
    for sigma in range(5):
        new_data_volumes = generate_gaussian_random_numbers(mu, (sigma+1)*0.3, completed_requests_num)
        Sophon_rel_Fixed = SophonFixed(requests, new_data_volumes, candidate_routes, completed_requests_num)
        Sophon_rel_Flexible = SophonFlexible(completed_requests_num, mu, (sigma+1)*0.3, True)
        # print(Sophon_rel_Flexible)
        sigma_s.append((sigma+1)*0.3)
        Sophon_Fixed.append(Sophon_rel_Fixed)
        Sophon_Flexible.append(Sophon_rel_Flexible)
    print(Sophon_Fixed)
    print(Sophon_Flexible)

    heterogeneous_requests_results['sigma'] = sigma_s
    heterogeneous_requests_results['SophonFixed'] = Sophon_Fixed
    heterogeneous_requests_results['SophonFlexible'] = Sophon_Flexible
    pd.DataFrame(heterogeneous_requests_results).to_csv(
        os.getcwd() + '\\..\\Comparison\\results\\heterogeneous_requests_sigma.csv', index=False)

def adjust_thresholds_fidelity():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 20
    requests = ALL_REQUESTS[0:completed_requests_num]
    data_volumes = DATA_VOLUMES[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    # fidelity_threshold = [0.0000000001, 0.000000001, 0.00000001, 0.0000001, 0.000001]
    fidelity_threshold = [0.0000001+(i*0.00000005) for i in range(19)]
    # fidelity_threshold = [0.1*i for i in range(21)]
    ft_s = []
    Sophon_Fixed = []
    Sophon_Flexible = []
    for ft in fidelity_threshold:
        rel_fixed = 0
        rel_flexible = 0
        for i in range(50):
            Sophon_rel_Fixed = SophonFixed(requests, data_volumes, candidate_routes, completed_requests_num,
                                           fidelity_threshold=ft)
            Sophon_rel_Flexible = SophonFlexible(completed_requests_num, heterogeneous=False, fidelity_threshold=ft)
            rel_fixed += Sophon_rel_Fixed
            rel_flexible += Sophon_rel_Flexible

        ft_s.append(ft)
        Sophon_Fixed.append(rel_fixed/50)
        Sophon_Flexible.append(rel_flexible/50)
        print("fidelity_threshold is :" + str(ft))

    heterogeneous_requests_results = {}
    heterogeneous_requests_results['fidelity_threshold'] = ft_s
    heterogeneous_requests_results['SophonFixed'] = Sophon_Fixed
    heterogeneous_requests_results['SophonFlexible'] = Sophon_Flexible
    pd.DataFrame(heterogeneous_requests_results).to_csv(
        os.getcwd() + '\\..\\Comparison\\results\\adjust_threshold_fidelity.csv', index=False)

def adjust_thresholds_delay():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 20
    requests = ALL_REQUESTS[0:completed_requests_num]
    data_volumes = DATA_VOLUMES[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    # delay_threshold = [120, 135, 150, 165, 180]
    delay_threshold = [i for i in range(16, 37)]
    dt_s = []
    Sophon_Fixed = []
    Sophon_Flexible = []
    for dt in delay_threshold:
        Sophon_rel_Fixed = SophonFixed(requests, data_volumes, candidate_routes, completed_requests_num,
                                       delay_threshold=dt)
        Sophon_rel_Flexible = SophonFlexible(completed_requests_num, heterogeneous=False, delay_threshold=dt)

        dt_s.append(dt)
        Sophon_Fixed.append(Sophon_rel_Fixed)
        Sophon_Flexible.append(Sophon_rel_Flexible)
        print("delay_threshold is :" + str(dt))

    heterogeneous_requests_results = {}
    heterogeneous_requests_results['delay_threshold'] = dt_s
    heterogeneous_requests_results['SophonFixed'] = Sophon_Fixed
    heterogeneous_requests_results['SophonFlexible'] = Sophon_Flexible
    pd.DataFrame(heterogeneous_requests_results).to_csv(
        os.getcwd() + '\\..\\Comparison\\results\\adjust_threshold_delay.csv', index=False)

def obtain_communication_threshold():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 200
    requests = ALL_REQUESTS[0:completed_requests_num]
    data_volumes = DATA_VOLUMES[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        while (shortest_paths == None) or (len(shortest_paths[1])!=QNConfig.candidate_route_num):
            requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    initial_communication_threshold = 0
    interval = 1
    rel = []
    ct = []
    for time in range(100):
        # print(time)
        communication_threshold = initial_communication_threshold + time*interval
        ct.append(communication_threshold)
        completed_request_num = SophonFixed_communication_threshold(requests, data_volumes, candidate_routes,
                                                                    completed_requests_num, communication_threshold)
        print("Threshold is " + str(communication_threshold) + "-----the comleted request num is " + str(completed_request_num))
        rel.append(completed_request_num)
    results = {}
    results['communication_threshold'] = ct
    results['completed_request_num'] = rel
    pd.DataFrame(results).to_csv(
        os.getcwd() + '\\..\\Comparison\\results\\adjust_threshold_communication_45.csv', index=False)

def obtain_computing_threshold():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    completed_requests_num = 200
    requests = ALL_REQUESTS[0:completed_requests_num]
    data_volumes = DATA_VOLUMES[0:completed_requests_num]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                           QNConfig.candidate_route_num, weight=customed_weight)
        while shortest_paths == None:
            requests[r_id] = random.sample(range(1, QNConfig.node_num), 2)
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]

    for i in range(completed_requests_num):
        if len(candidate_routes[i]) != QNConfig.candidate_route_num:
            for crn in range(QNConfig.candidate_route_num - 1):
                candidate_routes[i].append(candidate_routes[i][0])

    initial_computing_threshold = 0
    interval = 45
    rel = []
    ct = []
    for time in range(100):
        # print(time)
        computing_threshold = (initial_computing_threshold + time * interval) * 0.001
        ct.append(computing_threshold)
        completed_request_num = SophonFlexible_computing_threshold(completed_requests_num, computing_threshold)
        print("Computing Threshold is " + str(computing_threshold) + "-----the comleted request num is " + str(
            completed_request_num))
        rel.append(completed_request_num)
    results = {}
    results['communication_threshold'] = ct
    results['completed_request_num'] = rel
    pd.DataFrame(results).to_csv(
        os.getcwd() + '\\..\\Comparison\\results\\adjust_threshold_computing_45.csv', index=False)


if __name__ == '__main__':
    # -----------different scales of the request set with a fixed topology----------------
    # baseline_comparison_fixed_topology()
    # -----------different scales of the topology with a fixed number of requests-------------------
    baseline_comparison_fixed_request()


    # --------使用R=5的训练完成代理，修改request_pool_size和learning_rate大小
    # heterogeneous_requests_mu()
    # heterogeneous_requests_sigma()
    # adjust_thresholds_fidelity()
    # adjust_thresholds_delay()
    # ---------------------------topology scale------------------------
    # 1. 200 requests
    # 2. 修改不同scales的 ``Topology/topology.csv''，控制不同拓扑的读入
    # 3. 修改QNEnv下的不同scals下的QNModel
    # 4. 修改Config/TopologyConfig.py中的node_num参数
    # 5. 修改Agent加载的智能体文件路径, Provisioning/Agent.py 中的self.model.load_state_dict对应的Comparison/TrainedModel下的文件夹名
    # 6. 修改不同规模拓扑结构时，在requests.py文件中修改基于不同拓扑结构的请求集合ALL_REQUESTS
    # obtain_communication_threshold()
    # obtain_computing_threshold()






