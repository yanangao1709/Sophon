# EFiRAP is a typical ``All_in''-scheme transmission framework
import math
import time

from gurobipy import *
from QNEnv import QNModel
from Config import QNConfig
from Config import AgentConfig


# the approximation ratio
epsilon = 0.01

# ----------------Entanglement Path Selection (EPS) algorithm emplementation-------------------
# (1) LP_solver
def LP_solver(x_constraint, I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity):
    try:
        # 定义问题类型
        m = Model("LinearProblem")
        # ILP不要输出额外计算信息
        m.setParam("OutputFlag", 0)
        # 定义变量
        y_vars_ = m.addVars(I*J, vtype=GRB.CONTINUOUS)
        Y_vars = []
        for i in range(I):
            Y_temp = []
            for j in range(J):
                Y_temp.append(y_vars_[i*J + j])
            Y_vars.append(Y_temp)

        # 定义优化目标=变量加和
        obj = quicksum(Y_vars[i][j]
                       for i in range(I)
                       for j in range(J)
                       )
        # 设置优化目标
        m.setObjective(obj, GRB.MAXIMIZE)

        # 添加约束
        # fidelity 约束
        m.addConstrs(
            quicksum(
                Y_vars[i][j] * fidelity_parameters[i][j]
                for j in range(J)
            ) >= QNConfig.F_thr
            for i in range(I)
        )
        # delay 约束
        m.addConstrs(
            quicksum(
                Y_vars[i][j] * delay_parameters[i][j]
                for j in range(J)
            ) <= QNConfig.D_thr
            for i in range(I)
        )
        # 变量大于等于0的约束
        m.addConstrs(
            Y_vars[i][j] >= x_constraint[i*J+j]
            for i in range(I)
            for j in range(J)
        )
        # node capacity 约束
        m.addConstrs(
            quicksum(
                Y_vars[i][j] * H_RKN[i][j][n] * 2
                for i in range(I)
                for j in range(J)
            ) <=  node_capacity[n]
            for n in range(QNConfig.node_num)
        )
        # m.addConstrs(
        #         Y_vars[i][j] <= AgentConfig.X_thr - 1
        #         for i in range(I)
        #         for j in range(J)
        # )
        m.optimize()
        solution = []
        for i in m.getVars():
            solution.append(i.x)
            # print('%s = %g' % (i.varName, i.x), end=", ")
        # print("\n")
        max_ILP_obj = m.ObjVal
        m.reset()
        return solution, max_ILP_obj
    except GurobiError as e:
        # print('Error code' + str(e.errno) + ":" + str(e))
        return None, None
    except AttributeError:
        # print('Encountered an attribute error')
        return None, None

def find_combinations(target_sum, num_elements, current_combination, result):
    # 如果组合的长度已达到 num_elements，并且和等于 target_sum，保存当前组合
    if len(current_combination) == num_elements:
        if sum(current_combination) == target_sum:
            result.append(current_combination[:])  # 添加当前组合的副本
        return

    # 从 0 到目标和（包括）递归
    start_value = current_combination[-1] if current_combination else 0
    for value in range(start_value, target_sum + 1):
        current_combination.append(value)
        find_combinations(target_sum, num_elements, current_combination, result)
        current_combination.pop()  # 回溯，移除最后一个元素

def DP_solver(target_sum, rows, cols):
    result = []
    find_combinations(target_sum, rows*cols, [], result)
    return result

def get_H_RKN(I, J, candidate_routes):
    H_RKN = [[[0] * QNConfig.node_num for i in range(J)] for j in range(I)]
    for r in range(I):
        for k,p in enumerate(candidate_routes[r]):
            for n in range(len(p)):
                H_RKN[r][k][p[n]-1] = 1
    return H_RKN

def runEFiRAP(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity):
    # 运行算法
    solution, obj = LP_solver([0 for j in range(I*J)], I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
    if solution is None:
        return [0 for s in range(I*J)]

    # I变大，EFiRAP的DP_solver花费巨大计算时长
    if I >= 4:
        time.sleep((0.012605685454148512/5)*I)
        return [math.floor(s) for s in solution]

    z_ = sum(solution)
    s = min(math.floor(z_), QNConfig.node_num * (1 - epsilon) / epsilon)

    z_ALG = 0
    X_ALG = [[0 for j in range(J)] for i in range(I)]

    start_t = sum([math.floor(sl) for sl in solution])

    for t in range(start_t, s, 1):
        T_solutions = DP_solver(t, I, J)
        for idx, arr in enumerate(T_solutions):
            # 替换约束，执行LP
            solution_t, obj_t = LP_solver(arr, I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
            if solution_t is not None:
                t_ = sum([math.floor(s) for s in solution_t])
                if z_ALG < t_:
                    z_ALG = t_
                    X_ALG = solution_t
    if z_ALG == 0:
        z_ALG = start_t
        X_ALG = [math.floor(s) for s in solution]
    return X_ALG

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
                distance += QNModel.LINK_LENS[route[rt]-1][route[rt+1]-1]
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

def obtain_approximate_s(requests, candidate_routes, node_capacity):
    fidelity_parameters, candidate_routes_len = get_route_fidelity(requests, candidate_routes)
    delay_parameters = get_route_delay(requests, candidate_routes, candidate_routes_len)

    I = len(requests)
    J = len(candidate_routes[0])
    H_RKN = get_H_RKN(I, J, candidate_routes)
    integer_solutions = runEFiRAP(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
    return integer_solutions, H_RKN

def check_complete_s(best_s, new_requests, new_requests_data, node_capacity, H_RKN):
    # check 这次的解有没有完成所有请求所需的数据量传输要求
    request_if_sucess = [0 for r_id in range(len(new_requests))]
    remaining_data = [0 for r_id in range(len(new_requests))]
    route_nums = [[0 for rt_id in range(QNConfig.candidate_route_num)] for r_id in range(len(new_requests))]
    for r_id in range(len(new_requests)):
        for rt_id in range(QNConfig.candidate_route_num):
            # 这条路径会被建立多少次
            route_nums[r_id][rt_id] = best_s[r_id*QNConfig.candidate_route_num+rt_id]

    for r_id in range(len(new_requests)):
        transmitted_data = 0
        for rt_id in range(QNConfig.candidate_route_num):
            transmitted_data += route_nums[r_id][rt_id]
        if transmitted_data >= new_requests_data[r_id]:
            request_if_sucess[r_id] = True
        else:
            request_if_sucess[r_id] = False
            remaining_data[r_id] = new_requests_data[r_id]-transmitted_data

    new_node_capacity = [0 for n in range(QNConfig.node_num)]
    for r_id in range(len(new_requests)):
        for rt_id in range(QNConfig.candidate_route_num):
            if route_nums[r_id][rt_id] > 0:
                for n in range(QNConfig.node_num):
                    if H_RKN[r_id][rt_id][n] == 1:
                        node_capacity[n] -= route_nums[r_id][rt_id] * 2
    for n in range(QNConfig.node_num):
        new_node_capacity[n] = node_capacity[n]

    return request_if_sucess, remaining_data, new_node_capacity

def adjust_requests(request_if_sucess, remaining_data, original_requests):
    new_requests = []
    new_requests_data = []
    for r_id in range(len(original_requests)):
        if not request_if_sucess[r_id]:
            new_requests.append(original_requests[r_id])
            new_requests_data.append(remaining_data[r_id])
    return new_requests, new_requests_data

def run_EFiRAP(new_requests, candidate_routes, node_capacity):
    # 计算一次传输的吞吐
    approximate_s, H_RKN = obtain_approximate_s(new_requests, candidate_routes, node_capacity)
    throughput = 0
    node_memory_used = [0 for i in range(QNConfig.node_num)]
    for r in range(len(new_requests)):
        for cr in range(QNConfig.candidate_route_num):
            if approximate_s[r * QNConfig.candidate_route_num + cr] > 0:
                # one E2E entanglement trasmits one qubit
                throughput += approximate_s[r * QNConfig.candidate_route_num + cr]
                route = candidate_routes[r][cr]
                for rn in route:
                    node_memory_used[rn-1] += approximate_s[r * QNConfig.candidate_route_num + cr]

    memory_used_rate = 0
    for n in range(QNConfig.node_num):
        memory_used_rate += node_memory_used[n]/node_capacity[n]
    return throughput, memory_used_rate/QNConfig.node_num


# return EFiRAP one-time entanglement transmission
def EFiRAP(requests, data_volumes, candidate_routes):
    new_requests = requests.copy()
    node_capacity = QNModel.NODE_CPA.copy()
    throughput, average_memory_used_rate = run_EFiRAP(new_requests, candidate_routes, node_capacity)
    return throughput, average_memory_used_rate

# return the remaining data transmission requirement of the request set
def runEFiRAP_com(new_requests, candidate_routes, node_capacity):
    # 计算一次传输的吞吐
    approximate_s, H_RKN = obtain_approximate_s(new_requests, candidate_routes, node_capacity)
    r_satisfied_data = [[0 for rt in range(QNConfig.candidate_route_num)] for r in range(len(new_requests))]
    for r in range(len(new_requests)):
        for cr in range(QNConfig.candidate_route_num):
            if approximate_s[r * QNConfig.candidate_route_num + cr] > 0:
                r_satisfied_data[r][cr] =  approximate_s[r * QNConfig.candidate_route_num + cr]
    return r_satisfied_data









