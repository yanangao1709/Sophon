# 中心化的branch and bound算法实现步骤：
# 1. 遍历所有请求的解，如果请求中的变量值，存在Y_var[r][route] == 1, 则直接给该请求分配路径route;否则，将该请求的所有Y_var[r][*]压入列表，等待branch and bound
# 2. 对list中所有的Y_var值，取最大，作为当前branch节点的请求r_branch
# 3. 判断在确定了步骤1中请求的基础上，看看r_branch的候选路径还有几条是feasible的（即，用约束判断并记录），如果剩下一条，则标记；如果没有则此枝无解，剪掉；如果大于1，则进入路径节点级别的branch and bound
# 4. 递归调用节点级的branch and bound,从多条可行路径中，查找feasible路径
# 5. 描述不清晰的地方，联系gaoyn1709@163.com

# ILP-->LP-->Branch and Bound
from QNEnv import QNModel_1
from gurobipy import *
from Config import QNConfig
import random

def transmit_BB(self, all_agent_envs, all_agent_action):
    try:
        # 定义问题类型
        m = Model("LinearProblem")
        # 让ILP不要输出一些计算信息
        m.setParam("OutputFlag", 0)
        # 定义变量
        Y_vars = self.addVar(m)

        # 定义优化目标
        obj = quicksum(Y_vars[r][k] * self.obtain_transmitting_data(all_agent_envs, all_agent_action, r, k)
                       for k in range(self.candidate_route_num)
                       for r in range(self.request_num)
                       )
        m.setObjective(obj, GRB.MAXIMIZE)

        # 添加约束
        # fidelity 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * self.obtain_route_fidelity(all_agent_envs, all_agent_action, r, k)
                for k in range(self.candidate_route_num)
            ) >= QNConfig.F_thr
            for r in range(self.request_num)
        )
        # delay 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * self.routes_len[r][k] + self.obtain_D_beforre(r)  # 确定完更新那条路径，更新每个r的delay累加
                for k in range(self.candidate_route_num)
            ) <= QNConfig.D_thr
            for r in range(self.request_num)
        )
        # node capacity 约束
        m.addConstrs(
            quicksum(
                Y_vars[r][k] * self.H_RKN[r][k][n] *
                (self.obtain_storing_info(all_agent_envs)[r][k] +
                 self.obtain_transmission_using(all_agent_envs, all_agent_action, r, k, n))
                for r in range(self.request_num)
                for k in range(self.candidate_route_num)
            ) <= self.node_cpa[n]
            for n in range(QNConfig.node_num)
        )
        # route selection
        m.addConstrs(
            quicksum(Y_vars[r][k]
                     for k in range(QNConfig.candidate_route_num)
                     ) <= 1
            for r in range(QNConfig.request_pool_len)
        )
        m.write("./Transmitting/RouteSelection.lp")
        m.optimize()
        solution = []
        for i in m.getVars():
            solution.append(i.x)
            print('%s = %g' % (i.varName, i.x), end=", ")
        print("\n")
        self.Y = self.transformY(solution)
        max_ILP_obj = m.ObjVal
        # print(self.Y)
        m.reset()
        return self.Y, max_ILP_obj
    except GurobiError as e:
        self.Flag = False
        print('Error code' + str(e.errno) + ":" + str(e))
    except AttributeError:
        self.Flag = False
        print('Encountered an attribute error')
