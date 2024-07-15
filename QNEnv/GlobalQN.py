# global quantum network 需要完成三个事情：
# 1. 基于provisioning resource and selected routes 完成传输
# 2. 更新传输过程完成后，所引起的参数变化
# 3. 判断有没有被完成的请求，需不需要释放相应资源，并完成新请求添加
# 4. 把全局网络信息的变化，分发到局部智能体下
from Config import QNConfig, AgentConfig
from QNEnv import QNTopologyModel
class GlobalQN():
    def __init__(self):
        self.payoff = [0 for n in range(QNConfig.node_num)]
        self.r_state = [False for r in range(QNConfig.request_pool_len)]    # 记录请求池内请求是否被完成
        self.r_success_counter = 0
        self.r_total_counter = QNConfig.request_pool_len
        self.QNTopology = QNTopologyModel.QNModel()
        self.success_r_data = 0

    def obtain_storing_info(self, all_agent_envs):
        storing_M = {}
        for agent_id in range(QNConfig.agent_num):
            storing_M[agent_id] = all_agent_envs[agent_id].obtain_M()
        return storing_M

    def complete_transmission(self, all_agent_envs, all_agent_action, Y):
        for r in range(QNConfig.request_pool_len):
            if 1 not in Y[r]:
                continue
            r_route = self.QNTopology.ROUTES[r][Y[r].index(1)]
            transmitting_data_in = 0
            for n_agent in r_route:
                if n_agent == r_route[-1]:    # 是终点，信息只有传入，没有传出
                    all_agent_envs[n_agent-1].update_M(r, transmitting_data_in)
                    break
                if n_agent == r_route[0]: # 是起点，信息只有传出，拟分配了多少资源传多少
                    X = all_agent_action[n_agent-1][r]
                else:   #  中间节点，已存储+传入-传出
                    if all_agent_action[n_agent-1][r] >= self.storing_M[n_agent-1][r] + transmitting_data_in:
                        X = self.storing_M[n_agent-1][r] + transmitting_data_in
                    else:
                        X = all_agent_action[n_agent-1][r]
                transmitting_data_in = X
                all_agent_envs[n_agent-1].update_M(r, X)

    def update_request_pool(self):
        # print("有请求被完成了，更新请求.......")
        self.r_total_counter += 1
        if True in self.r_state:
            self.QNTopology.update_request_pool_and_topology_info(self.r_state)

    def judge_request(self, all_agent_envs, Y):
        for r in range(QNConfig.request_pool_len):
            d_r = self.QNTopology.REQUESTSET[r][-1] - 1
            d_r_storing_M = self.storing_M[d_r][r]
            if d_r_storing_M >= self.QNTopology.D_VOLUMN[r]:  # 请求r完成了，释放资源，更新请求池
                self.r_state[r] = True
                self.r_success_counter += 1
                self.success_r_data += self.QNTopology.D_VOLUMN[r]
                for n in range(QNConfig.node_num):
                    all_agent_envs[n].release_M(r)
        self.update_request_pool()

    def obtain_local_payoff(self, all_agent_envs, all_agent_action, Y):
        # 每个节点给所有请求提供的存储资源和拟分配的传输资源，实际在传输过程中用上了多少
        # 路径有没有用上，分配给这条路径有多少资源
        self.storing_M = self.obtain_storing_info(all_agent_envs)
        local_payoff = {}
        for node in range(QNConfig.node_num):
            local_payoff[node] = 0
            for r in range(QNConfig.request_pool_len):
                if 1 not in Y[r]:
                    continue
                r_route = self.QNTopology.ROUTES[r][Y[r].index(1)]
                if node+1 in r_route:
                    local_payoff[node] += self.storing_M[node][r] + all_agent_action[node][r]
        return local_payoff

    def step(self, all_agent_envs, all_agent_action, Y, step):
        # print("Global network is updating....")
        # 全局状态更新需要完成：1. 将各节点拟配置的资源，根据选中的路径，完成传输
        #                   2. 实现各节点存储资源M的状态更新, 更新全局网络的存储状态
        #                   3. 判断是否有请求被完成传输，及时释放为其存储的资源，并填充请求池
        #                   4. 计算全局对分布式节点的局部payoff
        #                   5. 计算全局奖励lamda并返回
        local_payoff = self.obtain_local_payoff(all_agent_envs, all_agent_action, Y)  # 实现 4
        self.complete_transmission(all_agent_envs, all_agent_action, Y) # 实现 1， 2
        self.judge_request(all_agent_envs, Y)    # 实现 3
        # print("step=" + str(step) + "---成功的请求---" + str(self.r_success_counter) + "---总共处理的请求---" + str(self.r_total_counter))
        global_reward = self.r_success_counter   # 实现5
        done = False
        if step >= AgentConfig.step_limit:
            done = True
        return local_payoff, global_reward, done, self.QNTopology, self.r_state, self.success_r_data
