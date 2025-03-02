from Examples.All_in import *
from Examples.OneByOne import *
from Examples.At_most_one_route import *
from Examples.At_most_one_route_1 import *
from Examples.Topology_exp import *
from Topology import k_shortest_paths
import numpy as np

# 递归实现
def obtain_solutions(k):
    if k == 1:
        return [[0],[1],[2]]
    rel_v = obtain_solutions(k-1)
    res = []
    for u in rel_v:
        for v in [[0],[1],[2]]:
            t_v = u+v
            if len(t_v)%2 ==0 and t_v[-1] * t_v[-2] !=0: continue
            res.append(t_v)
    return res

def customed_weight(u, v, d):
    '''
    networkx single_source_dijkstra() weight function implementation
    :param u:
    :param v:
    :param d:
    :return:
    '''
    edge_wt = d.get("length", 1)
    return edge_wt

def generate_gaussian_random_numbers(mu, sigma, completed_requests_num, min_value=10, max_value=20):
    assert sigma * 3 < (max_value - min_value) / 2
    random_numbers = np.random.normal(mu, sigma, completed_requests_num)
    result = np.clip(random_numbers, min_value, max_value)
    results = []
    for r in result:
        results.append(int(r))
    return results

def run_compare():
    OBO_res = []
    AI_res = []
    AMOR_res = []
    AMOR_res_1 = []
    requests = [['A', 'C'], ['A', 'H'], ['B', 'G'], ['D', 'H'], ['F', 'H'], ['A', 'E']]
    # 10,100,变化的
    # request_required_data = [10,10,10,10,10,10]
    # request_required_data = [100,100,100,100,100,100]

    request_required_data = [128, 40, 10, 96, 189, 57]
    # 候选路径集
    candidate_routes = {}
    for r_id in range(len(requests)):
        shortest_paths = k_shortest_paths.k_shortest_paths(G_exp, requests[r_id][0], requests[r_id][1],
                                                           candidate_route_num, weight=customed_weight)
        candidate_routes[r_id] = shortest_paths[1]
    keys_to_keep = []
    for r_id in range(len(requests)):
        keys_to_keep.append(r_id)
        cr = {key: candidate_routes[key] for key in keys_to_keep if key in candidate_routes}
        OBO_res.append(OneByOne(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr))
        AI_res.append(All_in(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr))
        AMOR_res.append(At_most_one_route(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr))
        # AMOR_res_1.append(At_most_one_route_1(requests[0:r_id+1], request_required_data[0:r_id+1], cr))
        print("---------------------------------------------------------")
    print(OBO_res)
    print(AI_res)
    print(AMOR_res)
    # print(AMOR_res_1)

def run_compare_average():
    OBO_res = [0 for i in range(6)]
    AI_res = [0 for i in range(6)]
    AMOR_res = [0 for i in range(6)]
    requests = [['A', 'C'], ['A', 'H'], ['B', 'G'], ['D', 'H'], ['F', 'H'], ['A', 'E']]
    # 10,100,变化的
    # request_required_data = [10,10,10,10,10,10]
    # request_required_data = [100,100,100,100,100,100]
    for i in range(10):
        request_required_data = generate_gaussian_random_numbers(55, 1, 6, min_value=10, max_value=100)
        # 候选路径集
        candidate_routes = {}
        for r_id in range(len(requests)):
            shortest_paths = k_shortest_paths.k_shortest_paths(G_exp, requests[r_id][0], requests[r_id][1],
                                                               candidate_route_num, weight=customed_weight)
            candidate_routes[r_id] = shortest_paths[1]
        keys_to_keep = []
        for r_id in range(len(requests)):
            keys_to_keep.append(r_id)
            cr = {key: candidate_routes[key] for key in keys_to_keep if key in candidate_routes}
            OBO_res[r_id] += OneByOne(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr)
            AI_res[r_id] += All_in(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr)
            AMOR_res[r_id] += At_most_one_route(requests[0:r_id + 1], request_required_data[0:r_id + 1], cr)
        print("---------------------------------------------------------")
        print(OBO_res)
        print(AI_res)
        print(AMOR_res)
    for i in range(6):
        OBO_res[i] = OBO_res[i]/10
        AI_res[i] = AI_res[i]/10
        AMOR_res[i] = AMOR_res[i]/10

    print(OBO_res)
    print(AI_res)
    print(AMOR_res)

if __name__ == '__main__':
    run_compare()
    run_compare_average()
