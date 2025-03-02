# Multi-R contains two steps, names as STEP I and STEP II
import random

from gurobipy import *
from Config import QNConfig
from Config import AgentConfig
from QNEnv import QNModel
from Transmitting import utils


def solve_Lp_1(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity):
    try:
        # 定义问题类型
        m = Model("LinearProblem")
        # ILP不要输出额外计算信息
        m.setParam("OutputFlag", 0)
        # 定义变量
        y_vars_ = m.addVars(I * J, vtype=GRB.CONTINUOUS)
        Y_vars = []
        for i in range(I):
            Y_temp = []
            for j in range(J):
                Y_temp.append(y_vars_[i * J + j])
            Y_vars.append(Y_temp)

        # 定义优化目标
        obj = quicksum(Y_vars[i][j]
                       for i in range(I)
                       for j in range(J)
                       )
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
        # node capacity 约束
        m.addConstrs(
            quicksum(
                Y_vars[i][j] * H_RKN[i][j][n] * 2
                for i in range(I)
                for j in range(J)
            ) <= node_capacity[n]
            for n in range(QNConfig.node_num)
        )
        # route selection
        m.addConstrs(
            quicksum(Y_vars[i][j]
                     for j in range(J)
                     ) <= 1
            for i in range(I)
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
        # print('Error code' + str(e.errno) + ":" + str(e))
        return None, None, False
    except AttributeError:
        # print('Encountered an attribute error')
        return None, None, False

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
        if sum_cap > QNModel.NODE_CPA[n]:
            return False

def branch_and_bound(requests, candidate_routes, H_RKN, node_capacity, target_r, route, h_signals, fidelity_parameters, delay_parameters):
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
        new_solution, max_ILP_obj, _ = solve_Lp_1(len(requests), len(candidate_routes[0]), H_RKN, fidelity_parameters, delay_parameters, node_capacity)
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
        branch_and_bound(requests, candidate_routes, H_RKN, node_capacity, target_r, None, h_signals, fidelity_parameters, delay_parameters)
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
            branch_and_bound(requests, candidate_routes, H_RKN, node_capacity, target_r, next_route, h_signals)

def obtain_integer_solutions(requests, candidate_routes, H_RKN, node_capacity, solutions, fidelity_parameters, delay_parameters):
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
        branch_and_bound(requests, candidate_routes, H_RKN, node_capacity, sorted_solution[0].r, None, h_signals, fidelity_parameters, delay_parameters)
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

def get_H_RKN(I, J, candidate_routes):
    H_RKN = [[[0] * QNConfig.node_num for i in range(J)] for j in range(I)]
    for r in range(I):
        for k,p in enumerate(candidate_routes[r]):
            for n in range(len(p)):
                H_RKN[r][k][p[n]-1] = 1
    return H_RKN

def solve_Lp_2(I, H_RKN, fidelity_parameters, delay_parameters, node_capacity, selected_routes):
    try:
        # 定义问题类型
        m = Model("LinearProblem")
        # ILP不要输出额外计算信息
        m.setParam("OutputFlag", 0)
        # 定义变量
        y_vars_ = m.addVars(I, vtype=GRB.CONTINUOUS)
        Y_vars = []
        for i in range(I):
            Y_vars.append(y_vars_[i])

        # 定义优化目标=变量加和
        obj = quicksum(Y_vars[i]
                       for i in range(I)
                       )
        # 设置优化目标
        m.setObjective(obj, GRB.MAXIMIZE)

        # 未选择路径的请求分配0
        for i in range(I):
            if selected_routes[i] == -1:
                m.addConstr(Y_vars[i] == 0)

        # 添加约束
        # fidelity 约束
        m.addConstrs(
            Y_vars[i] * fidelity_parameters[i][selected_routes[i]] >= QNConfig.F_thr
            for i in range(I)
        )
        # delay 约束
        m.addConstrs(
            Y_vars[i] * delay_parameters[i][selected_routes[i]] <= QNConfig.D_thr
            for i in range(I)
        )
        # node capacity 约束
        m.addConstrs(
            quicksum(
                Y_vars[i] * H_RKN[i][selected_routes[i]][n] * 2
                for i in range(I)
            ) <= node_capacity[n]
            for n in range(QNConfig.node_num)
        )
        # m.addConstrs(
        #     Y_vars[i] <= AgentConfig.X_thr - 1
        #     for i in range(I)
        # )
        m.optimize()
        solution = []
        for i in m.getVars():
            solution.append(i.x)
            # print('%s = %g' % (i.varName, i.x), end=", ")
        # print("\n")
        max_ILP_obj = sum(solution)
        # max_ILP_obj = m.ObjVal
        m.reset()
        return solution, max_ILP_obj
    except GurobiError as e:
        return None, None
    except AttributeError:
        return None, None

def run_Mulit_R(requests, data_volumes, candidate_routes):
    fidelity_parameters, candidate_routes_len = get_route_fidelity(requests, candidate_routes)
    delay_parameters = get_route_delay(requests, candidate_routes, candidate_routes_len)
    I = len(requests)
    J = len(candidate_routes[0])
    H_RKN = get_H_RKN(I, J, candidate_routes)
    node_capacity = QNModel.NODE_CPA
    # STEP I, maximize the number of quantum-user pairs, select the appropriate route for each SD pair
    # constraints imposed by: 1) node memory/capacity; 2) fidelity; 3) delay; 4) only one route
    # 求解LP
    solutions, max_obj, _ = solve_Lp_1(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
    # branch-and-bound 小数解转整数解
    integer_solutions = obtain_integer_solutions(requests, candidate_routes, H_RKN, node_capacity, solutions, fidelity_parameters, delay_parameters)

    # STEP II, maximize the expected throughput of selected quantum-user pairs
    # for STEP I by determining the qubits assigned to possible paths form the path set
    # Reserve the qubits in the network assigned for the selected routes in STEP I
    # Then, solving STEP II
    selected_routes = [-1 for i in range(I)]
    for i in range(I):
        for j in range(J):
            if integer_solutions[i][j] == 1:
                selected_routes[i] = j
                break
    qubit_allocation = solve_Lp_2(I, H_RKN, fidelity_parameters, delay_parameters, node_capacity, selected_routes)

    return sum(qubit_allocation[0])

def run_Mulit_R_chaneable_request_requirement(requests, data_volumes, candidate_routes):
    fidelity_parameters, candidate_routes_len = get_route_fidelity(requests, candidate_routes)
    delay_parameters = get_route_delay(requests, candidate_routes, candidate_routes_len)
    I = len(requests)
    J = len(candidate_routes[0])
    H_RKN = get_H_RKN(I, J, candidate_routes)
    node_capacity = QNModel.NODE_CPA
    # STEP I, maximize the number of quantum-user pairs, select the appropriate route for each SD pair
    # constraints imposed by: 1) node memory/capacity; 2) fidelity; 3) delay; 4) only one route
    # 求解LP
    solutions, max_obj, _ = solve_Lp_1(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
    # branch-and-bound 小数解转整数解
    integer_solutions = obtain_integer_solutions(requests, candidate_routes, H_RKN, node_capacity, solutions,
                                                 fidelity_parameters, delay_parameters)

    # STEP II, maximize the expected throughput of selected quantum-user pairs
    # for STEP I by determining the qubits assigned to possible paths form the path set
    # Reserve the qubits in the network assigned for the selected routes in STEP I
    # Then, solving STEP II
    selected_routes = [-1 for i in range(I)]
    for i in range(I):
        for j in range(J):
            if integer_solutions[i][j] == 1:
                selected_routes[i] = j
                break
    qubit_allocation = solve_Lp_2(I, H_RKN, fidelity_parameters, delay_parameters, node_capacity, selected_routes)

    throughput = 0
    node_memory_used = [0 for i in range(QNConfig.node_num)]
    for r in range(len(requests)):
        if data_volumes[r] > qubit_allocation[0][r]:
            throughput += qubit_allocation[0][r]
        else:
            throughput += data_volumes[r]

    for i in range(I):
        if selected_routes[i] == -1:
            continue
        route = candidate_routes[i][selected_routes[i]]
        for rn in route:
            node_memory_used[rn - 1] += qubit_allocation[0][i]

    memory_used_rate = 0
    for n in range(QNConfig.node_num):
        memory_used_rate += node_memory_used[n]/node_capacity[n]
    return throughput, memory_used_rate/QNConfig.node_num

# return EFiRAP one-time entanglement transmission
def Multi_R(requests, data_volumes, candidate_routes):
    throughput, average_memory_used_rate = run_Mulit_R_chaneable_request_requirement(requests, data_volumes, candidate_routes)
    return throughput, average_memory_used_rate

#
def run_Mulit_R_com(requests, candidate_routes, node_capacity):
    fidelity_parameters, candidate_routes_len = get_route_fidelity(requests, candidate_routes)
    delay_parameters = get_route_delay(requests, candidate_routes, candidate_routes_len)
    I = len(requests)
    J = len(candidate_routes[0])
    H_RKN = get_H_RKN(I, J, candidate_routes)
    # STEP I, maximize the number of quantum-user pairs, select the appropriate route for each SD pair
    # constraints imposed by: 1) node memory/capacity; 2) fidelity; 3) delay; 4) only one route
    # 求解LP
    solutions, max_obj, _ = solve_Lp_1(I, J, H_RKN, fidelity_parameters, delay_parameters, node_capacity)
    # branch-and-bound 小数解转整数解
    if solutions is None:
        integer_solutions = [[0,0,0] for i in range(I)]
    else:
        # integer_solutions = [[0, 0, 0] for i in range(I)]
        # for i in range(I):
        #     r_pro = solutions[QNConfig.candidate_route_num*i:QNConfig.candidate_route_num*(i+1)-1]
        #     if all((x-0)<0.0001 for x in r_pro):
        #         continue
        #     else:
        #         integer_solutions[i][r_pro.index(max(r_pro))] = 1
        integer_solutions = obtain_integer_solutions(requests, candidate_routes, H_RKN, node_capacity, solutions,
                                                 fidelity_parameters, delay_parameters)

    # STEP II, maximize the expected throughput of selected quantum-user pairs
    # for STEP I by determining the qubits assigned to possible paths form the path set
    # Reserve the qubits in the network assigned for the selected routes in STEP I
    # Then, solving STEP II
    selected_routes = [-1 for i in range(I)]
    for i in range(I):
        for j in range(J):
            if integer_solutions[i][j] == 1:
                selected_routes[i] = j
                break
    qubit_allocation = solve_Lp_2(I, H_RKN, fidelity_parameters, delay_parameters, node_capacity, selected_routes)
    if qubit_allocation[0] is None:
        r_qubit_allocation = [0 for i in range(I)]
    else:
        r_qubit_allocation = [qubit_allocation[0][i] for i in range(I)]

    allocated_r_rt_data_one_time = [[0 for rt in range(QNConfig.candidate_route_num)] for r in range(I)]
    for i in range(I):
        for j in range(J):
            if integer_solutions[i][j] == 1:
                allocated_r_rt_data_one_time[i][j] = r_qubit_allocation[i]
            else:
                allocated_r_rt_data_one_time[i][j] = 0

    return allocated_r_rt_data_one_time
