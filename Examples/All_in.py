# 这是大多数吞吐量最大化的文章的核心思想，尽可能多地建立two-qubit纠缠，每个纠缠只能传输2个qubit，来最大化吞吐
# 求解最大化吞吐ILP问题时，遍历所有解来求取最优解
import itertools
from Examples.Topology_exp import *


def adjust_requests(request_if_sucess, remaining_data, original_requests):
    new_requests = []
    new_requests_data = []
    for r_id in range(len(original_requests)):
        if not request_if_sucess[r_id]:
            new_requests.append(original_requests[r_id])
            new_requests_data.append(remaining_data[r_id])
    return new_requests, new_requests_data

def check_complete_s(best_s, new_requests, new_requests_data):
    # check 这次的解有没有完成所有请求所需的数据量传输要求
    request_if_sucess = [0 for r_id in range(len(new_requests))]
    remaining_data = [0 for r_id in range(len(new_requests))]
    route_nums = [[0 for rt_id in range(candidate_route_num)] for r_id in range(len(new_requests))]
    for r_id in range(len(new_requests)):
        for rt_id in range(candidate_route_num):
            # 这条路径会被建立多少次
            route_nums[r_id][rt_id] = best_s[r_id * candidate_route_num + rt_id]

    for r_id in range(len(new_requests)):
        transmitted_data = 0
        for rt_id in range(candidate_route_num):
            transmitted_data += route_nums[r_id][rt_id]
        if transmitted_data >= new_requests_data[r_id]:
            request_if_sucess[r_id] = True
        else:
            request_if_sucess[r_id] = False
            remaining_data[r_id] = new_requests_data[r_id]-transmitted_data

    return request_if_sucess, remaining_data

def check_s(solution, new_requests, candidate_routes):
    # check约束
    route_nums = [[0 for rt_id in range(candidate_route_num)] for r_id in range(len(new_requests))]
    for r_id in range(len(new_requests)):
        for rt_id in range(candidate_route_num):
            # 这条路径会被建立多少次
            route_nums[r_id][rt_id] = solution[r_id*candidate_route_num+rt_id]

    # check 每个节点，只要有一个节点违反约束，此解不可行
    for n_id in range(len(nodes)):
        sum_resources_route_need = 0
        # 遍历所有路径，看看这些路径是不是经过这个点
        for r_id in range(len(new_requests)):
            routes = candidate_routes[r_id]
            for rt_id in range(candidate_route_num):
                route = routes[rt_id]
                if nodes[n_id] in route:
                    sum_resources_route_need += route_nums[r_id][rt_id]
        if sum_resources_route_need > node_capacity[nodes[n_id]]:
            return False
    return True

def obtain_s(new_requests, candidate_routes):
    num_solutions = len(new_requests) * candidate_route_num
    values = [0, 1, 2]
    candidate_solutions = list(itertools.product(values, repeat=num_solutions))
    max_obj = 0
    s_index = 0
    for cs in range(len(candidate_solutions)):
        obj = sum(candidate_solutions[cs])
        # 判断这个解是不是可行，即节点容量约束
        if check_s(candidate_solutions[cs], new_requests, candidate_routes):
            if obj > max_obj:
                max_obj = obj
                s_index = cs
    return candidate_solutions[s_index]

def All_in(requests, request_required_data, candidate_routes, recording_words = True):
    # 最大化数据传输量，每次求的最优解，需要多少次才能让请求所需数据量传输完成
    # 请求传输的所需数据量为4，所以整型变量x_ij最大取值为2，可能的取值为0，1，2
    # 遍历所有解，并从中找到最优解，解的个数为3^10=59049
    time_cost = 1
    flag = False
    new_requests = requests.copy()
    new_requests_data = request_required_data.copy()
    while not flag:
        # print(time_cost)
        # print(new_requests)
        # print(new_requests_data)
        best_s = obtain_s(new_requests, candidate_routes)
        request_if_sucess, remaining_data = check_complete_s(best_s, new_requests, new_requests_data)
        if False in request_if_sucess:    # 调整请求，进入下一次求解
            time_cost += 1
            new_requests, new_requests_data = adjust_requests(request_if_sucess, remaining_data, new_requests)
        else:
            flag = True
    if recording_words:
        print("All_in method cost " + str(time_cost) + " times")
    return time_cost

