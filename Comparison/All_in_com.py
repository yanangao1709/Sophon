# 由于example中的All_in方法用的是遍历全局最优，当问题规模增大时，该方法无法使用，所以使用branch-and-bound算法，重写All_in的求解过程
from Config import QNConfig
from QNEnv.QNModel import *
import itertools
from gurobipy import *
from Transmitting import utils


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
    route_nums = [[0 for rt_id in range(QNConfig.candidate_route_num)] for r_id in range(len(new_requests))]
    for r_id in range(len(new_requests)):
        for rt_id in range(QNConfig.candidate_route_num):
            # 这条路径会被建立多少次
            route_nums[r_id][rt_id] = best_s[r_id][rt_id]

    for r_id in range(len(new_requests)):
        transmitted_data = 0
        for rt_id in range(QNConfig.candidate_route_num):
            transmitted_data += route_nums[r_id][rt_id] * 2
        if transmitted_data >= new_requests_data[r_id]:
            request_if_sucess[r_id] = True
        else:
            request_if_sucess[r_id] = False
            remaining_data[r_id] = new_requests_data[r_id]-transmitted_data

    return request_if_sucess, remaining_data

def check_s(solution, new_requests, candidate_routes):
    # check约束
    route_nums = [[0 for rt_id in range(QNConfig.candidate_route_num)] for r_id in range(len(new_requests))]
    for r_id in range(len(new_requests)):
        for rt_id in range(QNConfig.candidate_route_num):
            # 这条路径会被建立多少次
            route_nums[r_id][rt_id] = solution[r_id*QNConfig.candidate_route_num+rt_id]

    # check 每个节点，只要有一个节点违反约束，此解不可行
    for n_id in range(QNConfig.agent_num):
        sum_resources_route_need = 0
        # 遍历所有路径，看看这些路径是不是经过这个点
        for r_id in range(len(new_requests)):
            routes = candidate_routes[r_id]
            for rt_id in range(QNConfig.candidate_route_num):
                route = routes[rt_id]
                if n_id+1 in route:
                    sum_resources_route_need += route_nums[r_id][rt_id]*2
        if sum_resources_route_need > NODE_CPA[n_id]:
            return False
    return True

def judge_is_feasible(r, k, h_signals , fidelity_parameters, delay_parameters, r_num):
    # 判断包含这段路径route的路径是否可行
    if fidelity_parameters[r][k] < QNConfig.F_thr:
        return False
    if delay_parameters[r][k] > QNConfig.D_thr:
        return False
    for n in range(QNConfig.node_num):
        sum_cap = 0
        for r_determined in range(r_num):
            if h_signals[r] > 0:
                k_determined = h_signals[r_determined]
                sum_cap += 2
            sum_cap += 2
        if sum_cap > NODE_CPA[n]:
            return False

def branch_and_bound(requests, candidate_routes, target_r, route, h_signals, fidelity_parameters, delay_parameters):
    # print("进来分支了。。。。。")
    # 执行步骤2
    routes = candidate_routes[target_r]
    candidate_route_num = len(routes)
    feasible_routes = {}
    # 判断当前这块分支路径是否可行，以及target_r中的所有路径中，包含这块分支的路径段的路径有哪些
    for rt in range(candidate_route_num):
        if utils.is_sublist(route, routes[rt]):
            if judge_is_feasible(target_r, rt, h_signals, fidelity_parameters, delay_parameters, len(requests)):
                feasible_routes[rt] = routes[rt]

    if len(feasible_routes) <= 1:
        if len(feasible_routes) == 1:   # 该分支上有一条可行路径，为target_r选中该条路径，重新计算剪枝后的LP的max_obj以选取最好的路径
            h_signals[target_r] = feasible_routes.keys()[0]    # 假设target_r被标记，以计算LP的优化目标
        else:
            h_signals[target_r] = 0
        if -1 not in h_signals:
            return
        new_solution, max_ILP_obj, _ = solve_Lp(requests, candidate_routes, fidelity_parameters, delay_parameters, h_signals)
        if not _: # LP 无解，剪枝
            return

        # 执行步骤1，确定下一个被执行的请求r, 遍历的是还没有被确定的所有请求
        solution_list = []
        for r in range(len(requests)):
            if h_signals[r] == -1:
                for k in range(candidate_route_num):
                    if new_solution[r*candidate_route_num + k] == 1:
                        h_signals[r] = k
                        break
                for k in range(candidate_route_num):
                    solution_list.append(utils.LP_solution(new_solution[r * candidate_route_num + k], r, candidate_routes[r][k]))
        if len(solution_list) == 0:
            return
        sorted_solution = sorted(solution_list, key=lambda solution_list: solution_list.solution)
        target_r = sorted_solution[0].r
        branch_and_bound(requests, candidate_routes, target_r, None, h_signals, fidelity_parameters, delay_parameters)
    else:
        # 有至少两条可行路径,将整条路径分解为单节点进行branch and bound确定路径中的分支节点
        overlap_point = QNConfig.candidate_route_num
        for rt in range(QNConfig.candidate_route_num):
            if rt == 0:
                continue
            overlap = utils.find_overlap_node(routes[rt-1], routes[rt])
            if overlap < overlap_point:
                overlap_point = overlap

        # check 各个路径加入下一个分支后，是否依然可行
        # 找到不同的节点，各自进行branch and bound
        next_branches = []
        for rt in range(QNConfig.candidate_route_num):
            if routes[rt][overlap_point] not in next_branches:
                next_branches.append(routes[rt][overlap_point])
        for nb in range(len(next_branches)):
            next_route = routes[0][0:overlap_point].append(next_branches[nb])
            branch_and_bound(requests, candidate_routes, target_r, next_route, h_signals)

def addVar(m, requests, candidate_routes):
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    y_vars = m.addVars(r_num * candidate_routes_num, vtype=GRB.CONTINUOUS)
    Y_vars = []
    for i in range(r_num):
        Y_temp = []
        for j in range(candidate_routes_num):
            Y_temp.append(y_vars[i * candidate_routes_num + j])
        Y_vars.append(Y_temp)
    return Y_vars

def obtain_route_len(requests, candidate_routes):
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    routes_len = [[0 for k in range(candidate_routes_num)] for r in
                  range(r_num)]
    for r in range(r_num):
        for k in range(candidate_routes_num):
            route = candidate_routes[r][k]
            distance = 0
            for rt in range(len(route)-1):
                distance += LINK_LENS[route[rt]-1][route[rt+1]-1]
            routes_len[r][k] = distance
    return routes_len

def get_route_fidelity(requests, candidate_routes):
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    candidate_routes_len = obtain_route_len(requests, candidate_routes)
    fidelity_parameters = [[0 for k in range(candidate_routes_num)] for r in
                           range(r_num)]
    for r in range(r_num):
        for k in range(candidate_routes_num):
            route_fidelity = 0
            route = candidate_routes[r][k]
            P_rke = math.exp(-1 * QNConfig.gamma * candidate_routes_len[r][k])
            for rt in range(len(route)-1):
                route_fidelity += 2 * QNConfig.p * math.pow((1-QNConfig.p), 2-1) * P_rke
            fidelity_parameters[r][k] = route_fidelity
    return fidelity_parameters, candidate_routes_len

def get_route_delay(requests, candidate_routes, candidate_routes_len):
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    delay_parameters = [[0 for k in range(candidate_routes_num)] for r in range(r_num)]
    for r in range(r_num):
        for k in range(candidate_routes_num):
            delay_parameters[r][k] = candidate_routes_len[r][k]
    return delay_parameters

def solve_Lp(requests, candidate_routes, fidelity_parameters, delay_parameters, h_signals=None):
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    try:
        # 定义问题类型
        m = Model("LinearProblem")
        # ILP不要输出额外计算信息
        m.setParam("OutputFlag", 0)
        # 定义变量
        Y_vars = addVar(m, requests, candidate_routes)

        # 定义优化目标, 随着branch and bound 变量的个数逐渐减少，但仍然为最大化优化目标
        obj = quicksum(Y_vars[r][k]
                       for k in range(candidate_routes_num)
                       for r in range(r_num)
                       )
        m.setObjective(obj, GRB.MAXIMIZE)

        # 为已经确定请求的变量赋值
        if h_signals:
            for r in range(r_num):
                if h_signals[r] > -1:
                    if h_signals[r] == 0:
                        for k in range(candidate_routes_num):
                            m.addConstr(Y_vars[r][k] == 0)
                    else:
                        determined_k = h_signals[r] - 1
                        for k in range(candidate_routes_num):
                            if determined_k == k:
                                m.addConstr(Y_vars[r][k] == 1)
                            else:
                                m.addConstr(Y_vars[r][k] == 0)

        # 添加约束
        # fidelity 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * fidelity_parameters[r][k]
                for k in range(candidate_routes_num)
                ) >= QNConfig.F_thr
            for r in range(r_num)
        )
        # delay 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * delay_parameters[r][k]
                for k in range(candidate_routes_num)
            ) <= QNConfig.D_thr
            for r in range(r_num)
        )
        # node capacity 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * 2
                for r in range(r_num)
                for k in range(candidate_routes_num)
            ) <= NODE_CPA[n]
            for n in range(QNConfig.node_num)
        )
        # route selection
        m.addConstrs(
            quicksum(Y_vars[r][k]
                     for k in range(candidate_routes_num)
                     ) <= 1
            for r in range(r_num)
        )
        m.optimize()
        solution =  []
        for i in m.getVars():
            solution.append(i.x)
            # print('%s = %g' % (i.varName, i.x), end=", ")
        # print("\n")
        max_ILP_obj = m.ObjVal
        m.reset()
        return solution, max_ILP_obj, True
    except GurobiError as e:
        Flag = False
        # print('Error code' + str(e.errno) + ":" + str(e))
        return None, None, False
    except AttributeError:
        Flag = False
        # print('Encountered an attribute error')
        return None, None, False

def obtain_integer_solutions(requests, candidate_routes, solutions, fidelity_parameters, delay_parameters):
    solution_list = []
    r_num = len(requests)
    candidate_routes_num = len(candidate_routes[0])
    h_signals = [-1 for r in range(r_num)]
    # 执行步骤1,将存在==1结果的请求对优先确定
    for r in range(r_num):
        flag = False
        for k in range(candidate_routes_num):
            if solutions[r * candidate_routes_num + k] == 1:
                h_signals[r] = k + 1
                flag = True
                break
        if not flag:
            for k in range(candidate_routes_num):
                solution_list.append(
                    utils.LP_solution(solutions[r * candidate_routes_num + k], r, candidate_routes[r][k]))

    if len(solution_list) != 0:
        # 不等于1的LP结果排序
        sorted_solution = sorted(solution_list, key=lambda solution_list: solution_list.solution)
        branch_and_bound(requests, candidate_routes, sorted_solution[0].r, None, h_signals, fidelity_parameters, delay_parameters)
    best_Y = h_signals.copy()

    Y = []
    for r in range(r_num):
        if best_Y[r] == 0:
            Y.append([0 for k in range(QNConfig.candidate_route_num)])
        else:
            y = []
            for k in range(QNConfig.candidate_route_num):
                if best_Y[r]-1 == k:
                    y.append(1)
                else:
                    y.append(0)
            Y.append(y)
    return Y

def obtain_approximate_s(requests, candidate_routes):
    fidelity_parameters, candidate_routes_len = get_route_fidelity(requests, candidate_routes)
    delay_parameters = get_route_delay(requests, candidate_routes, candidate_routes_len)

    # 求解LP
    solutions, max_obj, _ = solve_Lp(requests, candidate_routes, fidelity_parameters, delay_parameters)
    # branch-and-bound 小数解转整数解
    integer_solutions = obtain_integer_solutions(requests, candidate_routes, solutions, fidelity_parameters, delay_parameters)
    return integer_solutions

def All_in_approximate_optimal(requests, request_required_data, candidate_routes, recording_words = True):
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
        approximate_s = obtain_approximate_s(new_requests, candidate_routes)
        request_if_sucess, remaining_data = check_complete_s(approximate_s, new_requests, new_requests_data)
        if False in request_if_sucess:  # 调整请求，进入下一次求解
            time_cost += 1
            new_requests, new_requests_data = adjust_requests(request_if_sucess, remaining_data, new_requests)
        else:
            flag = True
    if recording_words:
        print("All_in method cost " + str(time_cost) + " times")
    return time_cost


def All_in_run(requests, request_required_data, candidate_routes):
    total_time_costs = 0
    total_time_costs += All_in_approximate_optimal(requests, request_required_data, candidate_routes, False)
    return total_time_costs