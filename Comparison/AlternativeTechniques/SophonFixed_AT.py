from Config import QNConfig
from Provisioning import Agent
from Comparison.AlternativeTechniques.Fixed_AT import GlobalEnvFixed, ILPFixed, LocalEnvFixed
from QNEnv import QNModel


def obtain_H_RKN(candidate_routes):
    requests_num = len(candidate_routes)
    H_RKN = [[[0] * QNConfig.node_num for i in range(QNConfig.candidate_route_num)] for j in range(requests_num)]
    for r in range(requests_num):
        for k, p in enumerate(candidate_routes[r]):
            for n in range(len(p)):
                H_RKN[r][k][p[n] - 1] = 1
    return H_RKN

def obtain_route_len(candidate_routes):
    requests_num = len(candidate_routes)
    routes_len = [[0 for k in range(QNConfig.candidate_route_num)] for r in range(requests_num)]
    for r in range(requests_num):
        for k in range(QNConfig.candidate_route_num):
            route = candidate_routes[r][k]
            rt_len = 0
            for rk in range(len(route) - 1):
                node = route[rk] - 1
                next_node = route[rk + 1] - 1
                rt_len += QNModel.LINK_LENS[node][next_node]
            routes_len[r][k] = rt_len
    return routes_len

def obtain_route_hops(candidate_routes):
    requests_num = len(candidate_routes)
    route_hops = [[0 for rt in range(QNConfig.candidate_route_num)] for r in range(requests_num)]
    for r in range(requests_num):
        for k in range(QNConfig.candidate_route_num):
            route = candidate_routes[r][k]
            route_hops[r][k] = len(route)
    return route_hops

# 加载已经训练好的分布式代理，由于代理的规模限制，
def SophonFixed(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests)/QNConfig.request_pool_len)
    for agent_id in range(QNConfig.agent_num):
        for p in range(parts):
            if p == 0:
                local_env = LocalEnvFixed.LocalEnv(agent_id, requests, data_volumes, candidate_routes)
                all_agent_envs[agent_id] = [local_env]
                all_agent_obs[agent_id] = [local_env.reset()]
            else:
                local_env = LocalEnvFixed.LocalEnv(agent_id, requests, data_volumes, candidate_routes)
                all_agent_envs[agent_id].append(local_env)
                all_agent_obs[agent_id].append(local_env.reset())

    # 每个episode初始化一个全局环境和一个传输过程
    H_RKN = obtain_H_RKN(candidate_routes)
    routes_len = obtain_route_len(candidate_routes)
    routes_hops = obtain_route_hops(candidate_routes)
    global_env = GlobalEnvFixed.GlobalEnv(requests, data_volumes, candidate_routes, H_RKN, routes_len, routes_hops)
    trans = ILPFixed.TransmissionDeploy(requests, candidate_routes, H_RKN, routes_len, routes_hops,
                                        fidelity_threshold, delay_threshold)

    completed_parts = [False for p in range(parts)]
    while True:
        all_agent_action = {}
        for agent_id in range(QNConfig.agent_num):
            agent = agents[agent_id]
            for p in range(parts):
                action = agent.get_action(all_agent_obs[agent_id][p])
                if p == 0:
                    all_agent_action[agent_id] = [action]
                else:
                    all_agent_action[agent_id].append(action)

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action, candidate_routes, completed_parts)
        # 全局环境更新
        r_success_counter, current_topology, completed_parts, throughput, average_memory_used_rate = global_env.update(all_agent_envs, all_agent_action, Y, True)
        return throughput, average_memory_used_rate
