# ILP-->LP-->Branch and Bound
from QNEnv import QNModel
from gurobipy import *
from Config import QNConfig
import random
from Transmitting import utils

class Transmission:
    def __init__(self):
        self.requests = QNModel.REQUESTSET
        self.request_num = QNConfig.request_pool_len
        self.candidate_route_num = QNConfig.candidate_route_num
        self.H_RKN = QNModel.H_RKN
        self.routes = QNModel.ROUTES
        self.routes_len = QNModel.ROUTES_LEN
        self.node_cpa = QNModel.NODE_CPA
        self.routes_hops = QNModel.ROUTES_HOPS
        self.delay_before = [0 for r in range(QNConfig.request_pool_len)]
        self.all_Y = []

        self.weight_parameters = {}
        self.h_signals = [-1 for r in range(QNConfig.request_pool_len)]
        self.best_Y = []

    def set_new_topology(self, new_topology):
        self.requests = new_topology.REQUESTSET
        self.routes = new_topology.ROUTES
        self.routes_len = new_topology.ROUTES_LEN
        self.H_RKN = new_topology.H_RKN
        self.routes_hops = new_topology.ROUTES_HOPS
        self.node_cpa = new_topology.Capacity_nodes

    def addVar(self, m):
        y_vars = m.addVars(self.request_num * self.candidate_route_num, vtype=GRB.CONTINUOUS)
        Y_vars = []
        for i in range(self.request_num):
            Y_temp = []
            for j in range(self.candidate_route_num):
                Y_temp.append(y_vars[i * self.candidate_route_num + j])
            Y_vars.append(Y_temp)
        return Y_vars

    def obtain_transmitting_data(self, all_agent_envs, all_agent_action, r, k):
        # 求请求r的第k条候选路径传输量
        transmitting_data = []
        for n in range(len(self.routes[r][k])-1):
            node = self.routes[r][k][n] - 1
            if n==0:    # 起始点
                transmitting_data.append(all_agent_action[node][r])
                continue
            storing_M = all_agent_envs[node].obtain_M()[r]
            if all_agent_action[node][r] >= storing_M + transmitting_data[n-1]:
                transmitting_data.append(storing_M + transmitting_data[n-1])
            else:
                transmitting_data.append(all_agent_action[node][r])

        return sum(transmitting_data)

    def obtain_route_fidelity(self, all_agent_envs, all_agent_action, r, k):
        route_fidelity = 0
        P_rke = math.exp(-1 * QNConfig.gamma * self.routes_len[r][k])
        transmitting_data = []
        for n in range(len(self.routes[r][k])-1):
            node = self.routes[r][k][n] - 1
            if n==0:
                transmitting_data.append(all_agent_action[node][r])
            else:
                storing_M = all_agent_envs[node].obtain_M()[r]
                if all_agent_action[node][r] >= storing_M + transmitting_data[n-1]:
                    transmitting_data.append(storing_M + transmitting_data[n-1])
                else:
                    transmitting_data.append(all_agent_action[node][r])
            route_fidelity += transmitting_data[n] * QNConfig.p * math.pow((1-QNConfig.p), all_agent_action[node][r]-1) * P_rke
        return route_fidelity

    def update_D_beforre(self, solution):
        for r in range(QNConfig.request_pool_len):
            for k in range(QNConfig.candidate_route_num):
                if solution[QNConfig.candidate_route_num*r+k] == 1:
                    self.delay_before[r] = self.delay_before[r] + self.routes_len[r][k]
                    break

    def obtain_D_beforre(self, r):
        return self.delay_before[r]

    def obtain_transmission_using(self, all_agent_envs, all_agent_action, r, k, n):
        if n+1 not in self.routes[r][k]:
            return 0

        # 节点n是请求r的起点
        if n+1 == self.requests[r][0]:
            using_data = all_agent_action[n][r]
            return using_data
        # 终点不需要存储，直接传给应用端
        if n+1 == self.requests[r][1]:
            using_data = 0
            return using_data

        pos = self.routes[r][k].index(n+1)
        transmitting_data = []
        for nn in range(len(self.routes[r][k]) - 1):
            node = self.routes[r][k][nn] - 1
            if nn==0:
                transmitting_data.append(all_agent_action[node][r])
                continue
            storing_M = all_agent_envs[node].obtain_M()[r]
            if all_agent_action[node][r] >= storing_M + transmitting_data[nn-1]:
                transmitting_data.append(storing_M + transmitting_data[nn-1])
            else:
                transmitting_data.append(all_agent_action[node][r])
        using_data = transmitting_data[pos-1] - transmitting_data[pos]
        return using_data

    def calculate_LP_weight_parameters(self, all_agent_envs, all_agent_action):
        # 存储LP权重参数，便于bound剪枝后的重新LP运算
        # 优化目标权重参数\fidelity约束参数\delay约束参数\节点容量参数
        obj_parameters = [[0 for k in range(QNConfig.candidate_route_num)] for r in range(QNConfig.request_pool_len)]
        fidelity_parameters = [[0 for k in range(QNConfig.candidate_route_num)] for r in
                               range(QNConfig.request_pool_len)]
        delay_parameters = [[0 for k in range(QNConfig.candidate_route_num)] for r in range(QNConfig.request_pool_len)]
        node_cap_parameters = [[[0 for n in range(QNConfig.node_num)] for k in range(QNConfig.candidate_route_num)]
                               for r in range(QNConfig.request_pool_len)]
        for r in range(QNConfig.request_pool_len):
            for k in range(QNConfig.candidate_route_num):
                obj_parameters[r][k] = self.obtain_transmitting_data(all_agent_envs, all_agent_action, r, k)
                fidelity_parameters[r][k] = self.obtain_route_fidelity(all_agent_envs, all_agent_action, r, k)
                delay_parameters[r][k] = self.routes_len[r][k]
                for n in range(QNConfig.node_num):
                    node_cap_parameters[r][k][n] = self.H_RKN[r][k][n] * (all_agent_envs[n].obtain_M()[r] +
                         self.obtain_transmission_using(all_agent_envs, all_agent_action, r, k, n))

        self.weight_parameters['obj'] = obj_parameters
        self.weight_parameters['fidelity'] = fidelity_parameters
        self.weight_parameters['delay'] = delay_parameters
        self.weight_parameters['node'] = node_cap_parameters

    def obtain_determined_r_cap(self, n):
        occuppied_cap = 0
        for r in range(QNConfig.request_pool_len):
            if self.h_signals[r] > 0:
                k = self.h_signals[r] - 1
                r_route = self.routes[r][k]
                if n in r_route:
                    occuppied_cap += self.weight_parameters['node'][r][k][n]
        return occuppied_cap

    def solve_Lp(self):
        try:
            # 定义问题类型
            m = Model("LinearProblem")
            # ILP不要输出额外计算信息
            m.setParam("OutputFlag", 0)
            # 定义变量
            Y_vars = self.addVar(m)

            # 定义优化目标, 随着branch and bound 变量的个数逐渐减少，但仍然为最大化优化目标
            obj = quicksum(Y_vars[r][k] * self.weight_parameters['obj'][r][k]
                           for k in range(self.candidate_route_num)
                           for r in range(self.request_num)
                           )
            m.setObjective(obj, GRB.MAXIMIZE)

            # 为已经确定请求的变量赋值
            for r in range(self.request_num):
                if self.h_signals[r] > -1:
                    if self.h_signals[r] == 0:
                        for k in range(self.candidate_route_num):
                            m.addConstr(Y_vars[r][k] == 0)
                    else:
                        determined_k = self.h_signals[r] - 1
                        for k in range(self.candidate_route_num):
                            if determined_k == k:
                                m.addConstr(Y_vars[r][k] == 1)
                            else:
                                m.addConstr(Y_vars[r][k] == 0)

            # 添加约束
            # fidelity 约束
            m.addConstrs(
                quicksum(
                    Y_vars[r][k] * self.weight_parameters['fidelity'][r][k]
                    for k in range(self.candidate_route_num)
                    ) >= QNConfig.F_thr
                for r in range(self.request_num)
            )
            # delay 约束
            m.addConstrs(
                quicksum(
                    Y_vars[r][k] * self.weight_parameters['delay'][r][k] + self.obtain_D_beforre(r)
                    for k in range(self.candidate_route_num)
                ) <= QNConfig.D_thr
                for r in range(self.request_num)
            )
            # node capacity 约束
            m.addConstrs(
                quicksum(
                    Y_vars[r][k] * self.weight_parameters['node'][r][k][n]
                    for r in range(self.request_num)
                    for k in range(self.candidate_route_num)
                ) <= self.node_cpa[n] - self.obtain_determined_r_cap(n)
                for n in range(QNConfig.node_num)
            )
            # route selection
            m.addConstrs(
                quicksum(Y_vars[r][k]
                         for k in range(QNConfig.candidate_route_num)
                         ) <= 1
                for r in range(QNConfig.request_pool_len)
            )
            # m.write("./Transmitting/RouteSelection.lp")
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
            self.Flag = False
            # print('Error code' + str(e.errno) + ":" + str(e))
            return None, None, False
        except AttributeError:
            self.Flag = False
            # print('Encountered an attribute error')
            return None, None, False

    def judge_is_feasible(self, r, k):
        # 判断包含这段路径route的路径是否可行
        if self.weight_parameters['fidelity'][r][k] < QNConfig.F_thr:
            return False
        if self.weight_parameters['delay'][r][k] + self.obtain_D_beforre(r) > QNConfig.D_thr:
            return False
        for n in range(QNConfig.node_num):
            sum_cap = 0
            for r_determined in range(QNConfig.request_pool_len):
                if self.h_signals[r] > 0:
                    k_determined = self.h_signals[r_determined] - 1
                    sum_cap += self.weight_parameters['node'][r_determined][k_determined][n]
            if n+1 != self.requests[r][1]:
                sum_cap += self.weight_parameters['node'][r][k][n]
            if sum_cap > self.node_cpa[n]:
                return False
        return True

    def branch_and_bound(self, target_r, route):
        # 执行步骤2
        routes = self.routes[target_r]
        feasible_routes = []
        # 判断当前这块分支路径是否可行，以及target_r中的所有路径中，包含这块分支的路径段的路径有哪些
        for rt in range(QNConfig.candidate_route_num):
            if utils.is_sublist(route, routes[rt]):
                if self.judge_is_feasible(target_r, rt):
                    feasible_routes.append(routes[rt])

        if len(feasible_routes) <= 1:
            original_h_signal = self.h_signals[target_r]
            if len(feasible_routes) == 1:   # 该分支上有一条可行路径，为target_r选中该条路径，重新计算剪枝后的LP的max_obj以选取最好的路径
                self.h_signals[target_r] = routes.index(feasible_routes[0]) + 1 # 假设target_r被标记，以计算LP的优化目标
            else:
                # if self.h_signals == -1:
                self.h_signals[target_r] = 0

            # 判断是否已经确定了所有请求，记录整数解的优化目标
            obj = 0
            if -1 not in self.h_signals:
                for r in range(QNConfig.request_pool_len):
                    if self.h_signals[r] > 0:
                        obj += self.weight_parameters['obj'][r][self.h_signals[r] - 1]
            if self.max_obj < obj:
                self.max_obj = obj
                return

            new_solution, max_ILP_obj, _ = self.solve_Lp()
            if not _: # LP 无解，剪枝
                return

            if self.max_obj > max_ILP_obj:    # 当前枝的最优LP解，小于记录局部整数最优解，剪枝
                self.h_signals[target_r] = original_h_signal
                return

            # 执行步骤1，确定下一个被执行的请求r, 遍历的是还没有被确定的所有请求
            solution_list = []
            for r in range(QNConfig.request_pool_len):
                if self.h_signals[r] == -1:
                    for k in range(QNConfig.candidate_route_num):
                        if new_solution[r*QNConfig.candidate_route_num + k] == 1:
                            self.h_signals[r] = k + 1
                            break
                    if self.h_signals[r] == -1:
                        flag = False
                        for k in range(QNConfig.candidate_route_num):
                            if new_solution[r * QNConfig.candidate_route_num + k] > 0 and new_solution[
                                r * QNConfig.candidate_route_num + k] < 1:
                                flag = True
                                break
                        if not flag:
                            self.h_signals[r] = 0
                        else:
                            for k in range(QNConfig.candidate_route_num):
                                solution_list.append(
                                    utils.LP_solution(new_solution[r * QNConfig.candidate_route_num + k], r,
                                                      self.routes[r][k]))
            if len(solution_list) == 0:
                return
            sorted_solution = sorted(solution_list, key=lambda solution_list: solution_list.solution, reverse=True)
            target_r = sorted_solution[0].r
            self.branch_and_bound(target_r, None)
        else:
            # 有至少两条可行路径,将整条路径分解为单节点进行branch and bound确定路径中的分支节点
            overlap_pos = 20  # 最大路径长度
            for rt in range(len(feasible_routes)):
                if rt == 0:
                    continue
                if route is None:
                    overlap_pos_route = utils.find_overlap_node(feasible_routes[rt - 1], feasible_routes[rt])
                else:
                    overlap_pos_route = utils.find_overlap_node(feasible_routes[rt - 1][len(route):],
                                                   feasible_routes[rt][len(route):])
                if overlap_pos_route < overlap_pos:
                    overlap_pos = overlap_pos_route
            if route is not None:
                overlap_pos += len(route)

            # check 各个路径加入下一个分支后，是否依然可行
            # 找到不同的节点，各自进行branch and bound
            next_branches = []
            for rt in range(len(feasible_routes)):
                if feasible_routes[rt][overlap_pos + 1] not in next_branches:
                    next_branches.append(feasible_routes[rt][overlap_pos + 1])
            for nb in range(len(next_branches)):
                nb_point = next_branches[nb]
                origin_r = feasible_routes[0][0:overlap_pos + 1]
                origin_r.append(nb_point)
                self.branch_and_bound(target_r, origin_r)

    def transmit(self, all_agent_envs, all_agent_action):
        self.best_Y.clear()
        # 提前计算LP参数，因为这些参数在反复迭代计算过程中，不更改
        self.calculate_LP_weight_parameters(all_agent_envs, all_agent_action)
        solution, max_ILP_obj, _ = self.solve_Lp()
        self.max_obj = 0

        while -1 in self.h_signals:
            solution_list = []
            # 执行步骤1,将存在==1结果的请求对优先确定
            for r in range(QNConfig.request_pool_len):
                for k in range(QNConfig.candidate_route_num):
                    if solution[r*QNConfig.candidate_route_num+k] == 1:
                        self.h_signals[r] = k + 1
                        break
                # 不存在=1的candidate_route，判断是不是全部candidate_route的solution为0
                if self.h_signals[r] == -1:
                    flag = False
                    for k in range(QNConfig.candidate_route_num):
                        if solution[r * QNConfig.candidate_route_num + k] > 0 and solution[
                            r * QNConfig.candidate_route_num + k] < 1:
                            flag = True
                            break
                    if not flag:
                        self.h_signals[r] = 0
                    else:
                        for k in range(QNConfig.candidate_route_num):
                            solution_list.append(
                                utils.LP_solution(solution[r * QNConfig.candidate_route_num + k], r,
                                              self.routes[r][k]))

            if len(solution_list) != 0:
                # 不等于1的LP结果排序
                sorted_solution = sorted(solution_list, key=lambda solution_list: solution_list.solution, reverse=True)
                target_r = sorted_solution[0].r
                self.branch_and_bound(target_r, None)
                if self.h_signals[target_r] == -1:
                    self.h_signals[target_r] = 0

        self.best_Y = self.h_signals.copy()

        Y =[]
        for r in range(QNConfig.request_pool_len):
            if self.best_Y[r] == 0:
                Y.append([0 for k in range(QNConfig.candidate_route_num)])
            else:
                y = []
                for k in range(QNConfig.candidate_route_num):
                    if self.best_Y[r]-1 == k:
                        y.append(1)
                    else:
                        y.append(0)
                Y.append(y)
        max_obj = 0
        for r in range(QNConfig.request_pool_len):
            if self.best_Y[r] > 0:
                k = self.best_Y[r] - 1
                max_obj += self.weight_parameters['obj'][r][k]

        # self.update_D_beforre(solution)
        self.weight_parameters.clear()
        self.h_signals.clear()
        self.h_signals = [-1 for r in range(QNConfig.request_pool_len)]
        return Y, max_obj

# --------------------------------遍历查找最优路径------------------------------------------------

    def enumerate_combinations(self, n, current_combination=None, index=0):
        # 如果current_combination是None，则初始化一个空的列表
        if current_combination is None:
            current_combination = []

        # 如果已经处理了所有的坑
        if index == n:
            self.all_Y.append(current_combination.copy())
            # 将当前组合添加到结果列表中（这里只是打印）
            # print('方案:', current_combination)
            return

            # 对于每个坑，尝试放置0, 1, 2, 3
        for i in range(QNConfig.candidate_route_num+1):
            # 将当前数字添加到组合中
            current_combination.append(i)
            # 递归处理下一个坑
            self.enumerate_combinations(n, current_combination, index + 1)
            # 回溯，移除当前数字以尝试下一个数字
            current_combination.pop()

    '''
    遍历结果，寻找最优解，以保证分布式方法的有效性
    '''
    def transmit_optimal(self, all_agent_envs, all_agent_action):
        self.enumerate_combinations(QNConfig.request_pool_len)
        best_y = [0 for rt in range(QNConfig.request_pool_len)]
        max_obj = 0
        for y in self.all_Y:    # 遍历1024个解
            flag = True
            # 判断约束
            # fidelity 约束
            for r in range(self.request_num):
                total_f = 0
                if y[r] == 0:
                    total_f = QNConfig.F_thr
                else:
                    k = y[r] - 1
                    total_f += self.obtain_route_fidelity(all_agent_envs, all_agent_action, r, k)
                if (total_f < QNConfig.F_thr):
                    flag = False
                    break

            if flag:
                # delay 约束
                for r in range(self.request_num):
                    total_d = 0
                    if y[r] == 0:
                        total_d = 0
                    else:
                        k = y[r] - 1
                        total_d += self.routes_len[r][k] + self.obtain_D_beforre(r)
                    if (total_d > QNConfig.D_thr):
                        flag = False
                        break
            if flag:
                # node capacity 约束
                for n in range(QNConfig.node_num):
                    total_r = 0
                    for r in range(self.request_num):
                        if y[r] == 0:
                            total_r = 0
                        else:
                            k = y[r] - 1
                            total_r += self.H_RKN[r][k][n] * (all_agent_envs[n].obtain_M()[r] +
                            self.obtain_transmission_using(all_agent_envs, all_agent_action, r, k, n))
                    if total_r > self.node_cpa[n]:
                        flag = False
                        break
            # 判断最优解，和最优Obj
            if flag:
                obj = 0
                for r in range(self.request_num):
                    if y[r] == 0:   # 没选路径
                        continue
                    k = y[r] - 1    # 选的路径
                    obj += self.obtain_transmitting_data(all_agent_envs, all_agent_action, r, k)
                if max_obj < obj:
                    max_obj = obj
                    best_y = [i_y for i_y in y]

        # print("........ILP有解.........解为：" + str(best_y) + "-----最大传输数据量为：" + str(max_obj))

        # 解的格式转化
        # [[1, 0, 0], [1, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 1]]
        self.Y = []
        for r in range(QNConfig.request_pool_len):
            yy = []
            if best_y[r] == 0:
                yy = [0,0,0]
                self.Y.append(yy)
            else:
                for k in range(1, QNConfig.candidate_route_num+1):
                    if best_y[r] == k:
                        for kk in range(0, QNConfig.candidate_route_num):
                            if kk == k-1:
                                yy.append(1)
                            else:
                                yy.append(0)
                self.Y.append(yy)
        return self.Y, max_obj
