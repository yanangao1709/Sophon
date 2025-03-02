# global quantum network 需要完成三个事情：
# 1. 基于provisioning resource and selected routes 完成传输
# 2. 更新传输过程完成后，所引起的参数变化
# 3. 判断有没有被完成的请求，需不需要释放相应资源，并完成新请求添加
# 4. 把全局网络信息的变化，分发到局部智能体下
from Config import QNConfig, AgentConfig
from QNEnv import QNTopologyModel
from QNEnv import QNModel

class GlobalQN():
    def __init__(self):
        self.payoff = [0 for n in range(QNConfig.node_num)]
        self.r_state = [False for r in range(QNConfig.request_pool_len)]    # 记录请求池内请求是否被完成
        self.r_success_counter = 0
        self.r_total_counter = QNConfig.request_pool_len
        self.QNTopology = QNTopologyModel.QNModel(QNModel.REQUESTSET, QNModel.D_VOLUMN,
                                                  QNModel.ROUTES, QNModel.ROUTES_LEN,
                                                  QNModel.H_RKN, QNModel.ROUTES_HOPS,
                                                  QNModel.NODE_CPA)
        self.success_r_data = 0

    def complete_transmission(self, all_agent_envs, all_agent_action, Y):
        for r in range(QNConfig.request_pool_len):
            if 1 not in Y[r]:
                continue
            r_route = self.QNTopology.ROUTES[r][Y[r].index(1)]
            for n_agent_id in range(len(r_route)-1):
                n_agent = r_route[n_agent_id]
                X_node_r = all_agent_action[n_agent - 1][r]
                if n_agent == r_route[0]:  # 是起点，信息只有传出，拟分配了多少资源传多少
                    X = X_node_r
                else:  # 中间节点，已存储+传入-传出
                    storing_M_r = all_agent_envs[n_agent - 1].obtain_M()[r]
                    if X_node_r >= storing_M_r:
                        X = storing_M_r
                    else:
                        X = X_node_r
                next_node = r_route[n_agent_id + 1]
                if n_agent_id > 0:
                    all_agent_envs[n_agent - 1].update_M_self(r, X)
                all_agent_envs[next_node - 1].update_M_next(r, X)

    def update_request_pool(self, exec = False):
        self.r_total_counter += 1
        if True in self.r_state:
            self.QNTopology.update_request_pool_and_topology_info(self.r_state, exec)

    def judge_request(self, all_agent_envs, exec = False):
        for r in range(QNConfig.request_pool_len):
            d_r = self.QNTopology.REQUESTSET[r][-1] - 1
            d_r_storing_M = all_agent_envs[d_r].obtain_M()[r]
            if d_r_storing_M >= self.QNTopology.D_VOLUMN[r]:  # 请求r完成了，释放资源，更新请求池
                self.r_state[r] = True
                self.r_success_counter += 1
                self.success_r_data += self.QNTopology.D_VOLUMN[r]
                for n in range(QNConfig.node_num):
                    all_agent_envs[n].release_M(r)
        if True in self.r_state:
            self.update_request_pool(exec)

    def step(self, all_agent_envs, all_agent_action, Y, step):
        self.r_state = [False for r in range(QNConfig.request_pool_len)]
        # print("Global network is updating....")
        # 全局状态更新需要完成：1. 将各节点拟配置的资源，根据选中的路径，完成传输
        #                   2. 实现各节点存储资源M的状态更新, 更新全局网络的存储状态
        #                   3. 判断是否有请求被完成传输，及时释放为其存储的资源，并填充请求池
        #                   5. 计算全局奖励并返回
        self.complete_transmission(all_agent_envs, all_agent_action, Y) # 实现 1， 2
        self.judge_request(all_agent_envs)    # 实现 3
        global_reward = self.r_success_counter   # 实现5
        done = False
        if step >= AgentConfig.step_limit:
            done = True
        return global_reward, done, self.QNTopology, self.success_r_data

