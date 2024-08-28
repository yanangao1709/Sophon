#  当测试部署模式为Fixed requests， 修改相应请求生成接口

from Comparison.data.requests import *
from Topology import k_shortest_paths, RouteGenerator
import pandas as pd
import os
from Comparison.OBO_com import *
from Comparison.All_in_com import *
from Comparison.SophonFixed_com import *
from Comparison.SophonFlexible_com import *
import datetime
import numpy as np

def customed_weight(u, v, d):
    edge_wt = d.get("length", 1)
    return edge_wt

def baseline_comparison():
    G_Compare = RouteGenerator.draw(os.getcwd() + "\\..\\Topology\\topology.csv")

    results = {}
    OBO_rlt = []
    All_in_rlt = []
    Sophon_Fixed_rlt = []
    Sophon_Flexible_rlt = []

    times = {}
    OBO_times = []
    All_in_times = []
    Sophon_Fixed_times = []
    Sophon_Flexible_times = []

    for time in range(10):
        requests = ALL_REQUESTS[0:(time+1)*QNConfig.request_pool_len]
        data_volumes = DATA_VOLUMES[0:(time+1)*QNConfig.request_pool_len]
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_Compare, requests[r_id][0], requests[r_id][1],
                                                               candidate_route_num_com, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]

        time_OBO_before = datetime.datetime.now().timestamp()
        OBO_rel = OBO_run(requests, data_volumes, candidate_routes)
        time_OBO_after = datetime.datetime.now().timestamp()
        OBO_times.append(time_OBO_after-time_OBO_before)

        time_All_in_before = datetime.datetime.now().timestamp()
        All_in_rel = All_in_run(requests, data_volumes, candidate_routes)
        time_All_in_after = datetime.datetime.now().timestamp()
        All_in_times.append(time_All_in_after - time_All_in_before)

        Sophon_Fixed_before = datetime.datetime.now().timestamp()
        Sophon_rel_Fixed = SophonFixed(requests, data_volumes, candidate_routes, (time+1)*QNConfig.request_pool_len)
        Sophon_Fixed_after = datetime.datetime.now().timestamp()
        Sophon_Fixed_times.append(Sophon_Fixed_after-Sophon_Fixed_before)

        Sophon_Flexible_before = datetime.datetime.now().timestamp()
        Sophon_rel_Flexible = SophonFlexible((time+1)*QNConfig.request_pool_len)
        Sophon_Flexible_after = datetime.datetime.now().timestamp()
        Sophon_Flexible_times.append(Sophon_Flexible_after - Sophon_Flexible_before)

        OBO_rlt.append(OBO_rel)
        All_in_rlt.append(All_in_rel)
        Sophon_Fixed_rlt.append(Sophon_rel_Fixed)
        Sophon_Flexible_rlt.append(Sophon_rel_Flexible)
        print("The number of requests is " + str((time+1)*QNConfig.request_pool_len) + ". The transmission times are: OBO (" + str(OBO_rel) +
              "),  All_in (" + str(All_in_rel) + "),  SophonFixed (" + str(Sophon_rel_Fixed) + "),  SophonFlexible ("
              + str(Sophon_rel_Flexible) + ").")
        print(
            "The number of requests is " + str((time + 1) * QNConfig.request_pool_len) + ". The calculation time is: OBO (" + str(OBO_times[-1]) +
            "),  All_in (" + str(All_in_times[-1]) + "),  SophonFixed (" + str(Sophon_Fixed_times[-1]) + "),  SophonFlexible ("
            + str(Sophon_Flexible_times[-1]) + ").\n")

    results["OBO"] = OBO_rlt
    results["All_in"] = All_in_rlt
    results["SophonFixed"] = Sophon_Fixed_rlt
    results["SophonFlexible"] = Sophon_Flexible_rlt
    pd.DataFrame(results).to_csv(os.getcwd() + '\\..\\Comparison\\results\\execute_transmission_times.csv', index=False)

    times['OBO'] = OBO_times
    times['All_in'] = All_in_times
    times['SophonFixed'] = Sophon_Fixed_times
    times['SophonFlexible'] = Sophon_Flexible_times
    pd.DataFrame(times).to_csv(os.getcwd() + '\\..\\Comparison\\results\\execute_transmission_time.csv', index=False)


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
                                                           candidate_route_num_com, weight=customed_weight)
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
                                                           candidate_route_num_com, weight=customed_weight)
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
                                                           candidate_route_num_com, weight=customed_weight)
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
                                                           candidate_route_num_com, weight=customed_weight)
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


if __name__ == '__main__':
    # baseline_comparison()
    # --------使用R=5的训练完成代理，修改request_pool_size和learning_rate大小
    # heterogeneous_requests_mu()
    # heterogeneous_requests_sigma()
    adjust_thresholds_fidelity()
    # adjust_thresholds_delay()






