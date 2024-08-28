import itertools
from QNEnv import QNModel
from Config import QNConfig

def check_complete_s(best_s, new_r_data):
    transmitted_data = sum(best_s)
    if transmitted_data >= new_r_data:
        return True, 0
    else:
        return False, new_r_data-transmitted_data

def check_s(solution, request_id, candidate_routes):
    # check约束
    # check 每个节点，只要有一个节点违反约束，此解不可行
    for n_id in range(QNConfig.node_num):
        sum_resources_route_need = 0
        # 遍历所有路径，看看这些路径是不是经过这个点
        routes = candidate_routes[request_id]
        for rt_id in range(QNConfig.candidate_route_num):
            route = routes[rt_id]
            if n_id+1 in route:
                sum_resources_route_need += solution[rt_id]
        if sum_resources_route_need > QNModel.NODE_CPA[n_id]:
            return False
    return True

def obtain_s(request_id, candidate_routes):
    num_solutions = QNConfig.candidate_route_num
    values = [0, 1, 2]
    candidate_solutions = list(itertools.product(values, repeat=num_solutions))
    max_obj = 0
    s_index = 0
    for cs in range(len(candidate_solutions)):
        obj = sum(candidate_solutions[cs])
        # 判断这个解是不是可行，即节点容量约束
        if check_s(candidate_solutions[cs], request_id, candidate_routes):
            if obj > max_obj:
                max_obj = obj
                s_index = cs
    return candidate_solutions[s_index]

def OneByOne(requests, request_required_data, candidate_routes, recording_words = True):
    # 一个请求一个请求的响应，一个请求需要一次性响应2条路径，如果不能，先响应能响应的，剩下的完成此次响应，释放资源，重新开始下一次响应
    time_cost = 0
    for r_id in range(len(requests)):
        flag = False
        new_r_data = request_required_data[r_id]
        while not flag:
            best_s = obtain_s(r_id, candidate_routes)
            flag, new_r_data = check_complete_s(best_s, new_r_data)
            time_cost += 1
    if recording_words:
        print("OneByOne method cost " + str(time_cost) + " times")
    return time_cost

def OBO_run(requests, request_required_data, candidate_routes):
    total_time_costs = 0
    total_time_costs += OneByOne(requests, request_required_data, candidate_routes, False)
    return total_time_costs
