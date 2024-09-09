from QNEnv.QNModel import ROUTES, NODE_CPA, LINK_LENS
from Config import AgentConfig, QNConfig, TopologyConfig

class LocalQN():
    def __init__(self, agent_id):
        self.agent_id = agent_id + 1
        self.obs_size = AgentConfig.obs_size
        self.act_size = AgentConfig.act_size
        self.obs = [0 for i in range(self.obs_size)]
        self.M = [0 for r in range(QNConfig.request_pool_len)]
        self.reward = 0
        self.routes = ROUTES

    def set_routes(self, routes):
        self.routes.clear()
        self.routes = routes

    def reset(self):
        # 请求r的所有候选路径有没有经过该节点
        for r in range(QNConfig.request_pool_len):
            for rt in range(len(self.routes[r])):
                if self.agent_id in self.routes[r][rt]:
                    self.obs[r*QNConfig.candidate_route_num + rt] = 1

        # 该节点的内存使用情况 + 剩余情况
        for r in range(QNConfig.request_pool_len):
            self.obs[QNConfig.request_pool_len * QNConfig.candidate_route_num + r] = self.M[r]
            # self.obs[r] = self.M[r]
        self.obs[QNConfig.request_pool_len * QNConfig.candidate_route_num + QNConfig.request_pool_len + 1] = NODE_CPA[self.agent_id-1] - sum(self.M)
        # self.obs[QNConfig.request_pool_len] = NODE_CPA[self.agent_id-1] - sum(self.M)

        # 节点的邻居情况
        pos = QNConfig.request_pool_len * QNConfig.candidate_route_num + QNConfig.request_pool_len + 1
        for n in range(TopologyConfig.node_num):
            if LINK_LENS[self.agent_id-1][n] != 0:
                self.obs[pos+n] = 1
        return self.obs

    def obtain_M(self):
        return self.M

    def update_M_next(self, r, X):
        self.M[r] = self.M[r] + X

    def update_M_self(self, r, X):
        self.M[r] = self.M[r] - X

    def release_M(self, r):
        self.M[r] = 0

    def get_obs(self, current_topology):
        # 全局传输过程完成后，引起了单智能体局部观察的改变
        # 请求r的所有候选路径有没有经过该节点
        for r in range(QNConfig.request_pool_len):
            for rt in range(len(current_topology.ROUTES[r])):
                if self.agent_id in current_topology.ROUTES[rt]:
                    self.obs[r * QNConfig.request_pool_len + rt] = 1

        # 该节点的内存使用情况 + 剩余情况
        for r in range(QNConfig.request_pool_len):
            self.obs[QNConfig.request_pool_len * QNConfig.candidate_route_num + r] = self.M[r]
            # self.obs[r] = self.M[r]

        self.obs[QNConfig.request_pool_len * QNConfig.candidate_route_num + QNConfig.request_pool_len + 1] =\
            NODE_CPA[self.agent_id - 1] - sum(self.M)
        # self.obs[QNConfig.request_pool_len] = NODE_CPA[self.agent_id - 1] - sum(self.M)

        # 节点的邻居情况
        pos = QNConfig.request_pool_len * QNConfig.candidate_route_num + QNConfig.request_pool_len + 1
        for n in range(TopologyConfig.node_num):
            if LINK_LENS[self.agent_id - 1][n] != 0:
                self.obs[pos + n] = 1
        return self.obs

    def get_local_reward(self, actions, Y, global_reward, current_topology):
        # 单智能体的个体成本 + 来自全局的奖励
        flag = False
        for r in range(QNConfig.request_pool_len):
            if 1 in Y[r]:
                flag = True
        if not flag:
            return 0
        memory_usage = 0
        for r in range(QNConfig.request_pool_len):
            if 1 in Y[r] and self.agent_id in current_topology.ROUTES[r][Y[r].index(1)]:
                memory_usage += self.M[r] + actions[r]
                self.reward += self.M[r] + actions[r]
                self.reward += global_reward
            else:
                self.reward -= self.M[r] + actions[r]
                self.reward -= global_reward
        return self.reward, memory_usage/NODE_CPA[self.agent_id-1]

    def step(self, actions, global_reward, current_topology, Y):
        # 当前智能体的动作，全局给当前智能体的回报
        # current_topology 在全局网络中，更新完了的拓扑信息
        next_obs = self.get_obs(current_topology)
        local_reward, memory_usage = self.get_local_reward(actions, Y, global_reward, current_topology)
        # print(local_reward)
        return next_obs, local_reward, memory_usage


