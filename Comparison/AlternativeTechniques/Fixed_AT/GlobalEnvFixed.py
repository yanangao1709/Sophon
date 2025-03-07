# global quantum network 需要完成三个事情：
# 1. 基于provisioning resource and selected routes 完成传输
# 2. 更新传输过程完成后，所引起的参数变化
# 3. 判断有没有被完成的请求，需不需要释放相应资源，并完成新请求添加
# 4. 把全局网络信息的变化，分发到局部智能体下
from Config import QNConfig, AgentConfig
from Comparison.AlternativeTechniques.Fixed_AT import QNTopologyModelFixed
from QNEnv import QNModel

class GlobalEnv():
    def __init__(self, requests, data_volumes, candidate_routes, H_RKN, routes_len, routes_hops):
        self.request_num = len(requests)
        self.payoff = [0 for n in range(QNConfig.node_num)]
        self.r_state = [False for r in range(self.request_num)]    # 记录请求池内请求是否被完成
        self.r_total_counter = QNConfig.request_pool_len
        self.QNTopology = {}
        self.success_r_data = {}
        self.r_success_counter = {}
        parts = int(len(requests)/QNConfig.request_pool_len)
        for p in range(parts):
            # 获取部分请求
            p_r = range(p*QNConfig.request_pool_len, (p+1)*QNConfig.request_pool_len)
            p_cr = {key%QNConfig.request_pool_len: candidate_routes[key] for key in candidate_routes if key in p_r}
            self.QNTopology[p] = QNTopologyModelFixed.QNModel(requests[p*QNConfig.request_pool_len: (p+1)*QNConfig.request_pool_len],
                                                         data_volumes[p*QNConfig.request_pool_len: (p+1)*QNConfig.request_pool_len],
                                                         p_cr,
                                                         routes_len[p*QNConfig.request_pool_len: (p+1)*QNConfig.request_pool_len],
                                                         H_RKN[p*QNConfig.request_pool_len: (p+1)*QNConfig.request_pool_len],
                                                         routes_hops[p*QNConfig.request_pool_len: (p+1)*QNConfig.request_pool_len],
                                                         QNModel.NODE_CPA)
            self.success_r_data[p] = 0
            self.r_success_counter[p] = 0

    def complete_transmission(self, all_agent_envs, all_agent_action, Y):
        throughput = 0
        # ------测试计算100个请求的决策吞吐是否满足节点的容量限制------
        # ------结论：实验存在内存溢出
        # for n in range(QNConfig.node_num):
        #     in_flow = 0
        #     n_used = 0
        #     # 求流出-流入
        #     for r in range(self.request_num):
        #         r_used = 0
        #         if 1 not in Y[r]:
        #             continue
        #         part = int(r / QNConfig.request_pool_len)
        #         r_route = self.QNTopology[part].ROUTES[r % QNConfig.request_pool_len][Y[r].index(1)]
        #         if n+1 in r_route:
        #             # 求取这条路径对n的消耗是多少
        #             # n节点分配给该请求的数据量
        #             if n+1 == r_route[0]: # 起点,没有存储占用
        #                 out = all_agent_action[n][part][r % QNConfig.request_pool_len]
        #                 in_flow += 0
        #                 r_used = out
        #             else:
        #                 storing_M_r = all_agent_envs[n][part].obtain_M()[r % QNConfig.request_pool_len]
        #                 in_flow += all_agent_action[r_route[r_route.index(n + 1) - 1] - 1][part][
        #                     r % QNConfig.request_pool_len]
        #                 if n+1 == r_route[-1]: # 终点
        #                     out = 0
        #                 else:
        #                     out = all_agent_action[n][part][r % QNConfig.request_pool_len]
        #                     if out >= storing_M_r + in_flow:
        #                         out = storing_M_r + in_flow
        #                 r_used = in_flow + storing_M_r - out
        #         n_used += r_used
        #     test = QNModel.NODE_CPA[n]
        #     if n_used > QNModel.NODE_CPA[n]:
        #         test = 1
        node_memory_used = [0 for i in range(QNConfig.node_num)]
        for r in range(self.request_num):
            if 1 not in Y[r]:
                continue
            part = int(r/QNConfig.request_pool_len)
            if self.r_success_counter[part] == QNConfig.request_pool_len:
                continue
            r_route = self.QNTopology[part].ROUTES[r % QNConfig.request_pool_len][Y[r].index(1)]
            # transmitting
            r_throughput = 0
            for n_agent_id in range(len(r_route)-1):
                n_agent = r_route[n_agent_id]
                X_node_r = all_agent_action[n_agent - 1][part][r%QNConfig.request_pool_len]
                if n_agent_id == 0: # 是起点，信息只有传出
                    r_throughput = X_node_r
                else:   #  中间节点，已存储+传入-传出
                    # （n_agent-1）节点中，该请求的存储资源+流入资源
                    storing_M_r = all_agent_envs[n_agent-1][part].obtain_M()[r%QNConfig.request_pool_len]
                    before_n_agent = r_route[n_agent_id-1]
                    r_in_n = all_agent_action[before_n_agent - 1][part][r%QNConfig.request_pool_len]
                    if X_node_r >= storing_M_r + r_in_n:
                        X_node_r = storing_M_r + r_in_n
                # 只记录一次传输中，真正传到终点的数据量
                if r_throughput > X_node_r:
                    r_throughput = X_node_r
                next_node = r_route[n_agent_id+1]
                if n_agent_id >= 0:
                    all_agent_envs[n_agent - 1][part].update_M_self(r%QNConfig.request_pool_len, X_node_r)
                all_agent_envs[next_node-1][part].update_M_next(r%QNConfig.request_pool_len, X_node_r)
            throughput += r_throughput
            for rn in r_route:
                node_memory_used[rn - 1] += r_throughput * 0.5

        memory_used_rate = 0
        for n in range(QNConfig.node_num):
            memory_used_rate += node_memory_used[n] / QNModel.NODE_CPA[n]
        return throughput, memory_used_rate/QNConfig.node_num

    def update_request_pool(self, Fixed, exec = False):
        # print("有请求被完成了，更新请求.......")
        self.r_total_counter += 1
        part = int(self.request_num / QNConfig.request_pool_len)
        for p in range(part):
            if self.r_success_counter[p] == QNConfig.request_pool_len:
                continue
            current_state = self.r_state[p*QNConfig.request_pool_len : (p+1)*QNConfig.request_pool_len]
            if True in current_state and False in current_state:
                self.QNTopology[p].update_request_pool_and_topology_info(current_state, Fixed, exec)

    def judge_request(self, all_agent_envs, Fixed, exec = False):
        for r in range(self.request_num):
            copy_body = [r]
            part = int(r / QNConfig.request_pool_len)
            if self.r_success_counter[part] == QNConfig.request_pool_len:
                continue
            r_pair = self.QNTopology[part].REQUESTSET[r%QNConfig.request_pool_len]
            d_r = r_pair[-1] - 1
            d_r_storing_M = all_agent_envs[d_r][part].obtain_M()[r%QNConfig.request_pool_len]
            for p_r_id in range(r%QNConfig.request_pool_len+1, QNConfig.request_pool_len):
                p_r_pair = self.QNTopology[part].REQUESTSET[p_r_id]
                if r_pair == p_r_pair:
                    d_r_storing_M += all_agent_envs[d_r][part].obtain_M()[p_r_id]
                    copy_body.append(part*QNConfig.request_pool_len + p_r_id)
            if d_r_storing_M >= self.QNTopology[part].D_VOLUMN[r % QNConfig.request_pool_len]:  # 请求r及其复制体完成，释放资源，更新请求池
                for cp in copy_body:
                    self.r_state[cp] = True
                    for n in range(QNConfig.node_num):
                        all_agent_envs[n][part].release_M(cp % QNConfig.request_pool_len)
                self.r_success_counter[part] += 1
                self.success_r_data[part] += self.QNTopology[part].D_VOLUMN[r % QNConfig.request_pool_len]
        if True in self.r_state:
            self.update_request_pool(Fixed, exec)

    def update(self, all_agent_envs, all_agent_action, Y, Fixed):
        self.r_state = [False for r in range(self.request_num)]
        throughput, average_memory_used_rate = self.complete_transmission(all_agent_envs, all_agent_action, Y)
        self.judge_request(all_agent_envs, Fixed, True)
        total_success_counter = 0
        for p in range(len(self.r_success_counter)):
            total_success_counter += self.r_success_counter[p]
        completed_parts = []
        for p in range(len(self.r_success_counter)):
            if self.r_success_counter[p] == QNConfig.request_pool_len:
                completed_parts.append(True)
            else:
                completed_parts.append(False)
        return total_success_counter, self.QNTopology, completed_parts, throughput, average_memory_used_rate

