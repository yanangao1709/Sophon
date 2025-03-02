from Config import QNConfig
from Provisioning import Agent
from Comparison.AlternativeTechniques.Fixed_AT import GlobalEnvFixed, ILPFixed, LocalEnvFixed
from QNEnv import QNModel
import math


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

def SophonFixed_QBER_2(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
                action = [2, 2, 2, 2, 2]
                if p == 0:
                    all_agent_action[agent_id] = [action]
                else:
                    all_agent_action[agent_id].append(action)

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action, candidate_routes, completed_parts)
        # obtain the link-level fidelity and transmission dimension
        QBER_number = 0
        r_average_route_QBER = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            QBER_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_QBER = 0
            for rt in range(len(route) - 1):
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt] - 1][route[rt + 1] - 1]))
                rt_fidelity = 1 / math.sqrt(2) * QNConfig.p * math.pow((1 - QNConfig.p), 2 - 1) * P_rke
                if 4 - 4 * 2 * (1 - rt_fidelity) < 0:
                    route_QBER += 0.5 - rt_fidelity
                else:
                    route_QBER += (2 - math.sqrt(4 - 4 * 2 * (1 - rt_fidelity))) / 4
            average_route_QBER = route_QBER / (len(route) - 1)
            r_average_route_QBER += average_route_QBER
        return r_average_route_QBER / QBER_number


def SophonFixed_QBER_flexible(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
        # obtain the link-level fidelity and transmission dimension
        QBER_number = 0
        r_average_route_QBER = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            QBER_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_QBER = 0
            for rt in range(len(route)-1):
                node = route[rt]-1
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt]-1][route[rt+1]-1]))
                rt_data = all_agent_action[node][int(r/QNConfig.request_pool_len)][r%QNConfig.request_pool_len]
                if rt_data == 0:
                    route_QBER += 0.5
                else:
                    rt_fidelity = 1/math.sqrt(rt_data) * QNConfig.p * math.pow((1-QNConfig.p), rt_data-1) * P_rke
                    if 4-4*2*(1-rt_fidelity) < 0:
                        route_QBER += 0.5 - rt_fidelity
                    else:
                        route_QBER += (2-math.sqrt(4-4*2*(1-rt_fidelity)))/4
            average_route_QBER = route_QBER/(len(route)-1)
            r_average_route_QBER += average_route_QBER
        return r_average_route_QBER/QBER_number

def SophonFixed_SNR_2(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
                action = [2, 2, 2, 2, 2]
                if p == 0:
                    all_agent_action[agent_id] = [action]
                else:
                    all_agent_action[agent_id].append(action)

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action, candidate_routes, completed_parts)
        # obtain the link-level fidelity and transmission dimension
        fidelity_number = 0
        r_average_route_SNR = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            fidelity_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_SNR = 0
            for rt in range(len(route) - 1):
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt] - 1][route[rt + 1] - 1]))
                rt_fidelity = 1 / math.sqrt(2) * QNConfig.p * math.pow((1 - QNConfig.p), 2 - 1) * P_rke
                route_SNR += rt_fidelity/(1-rt_fidelity)
            r_average_route_SNR += route_SNR/(len(route)-1)
        return r_average_route_SNR / fidelity_number

def SophonFixed_SNR_flexible(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
        # obtain the link-level fidelity and transmission dimension
        SNR_number = 0
        r_average_route_SNR = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            SNR_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_SNR= 0
            for rt in range(len(route) - 1):
                node = route[rt] - 1
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt] - 1][route[rt + 1] - 1]))
                rt_data = all_agent_action[node][int(r / QNConfig.request_pool_len)][r % QNConfig.request_pool_len]
                if rt_data == 0:
                    route_SNR += 0.5
                else:
                    rt_fidelity = 1 / math.sqrt(rt_data) * QNConfig.p * math.pow((1 - QNConfig.p), rt_data - 1) * P_rke
                    route_SNR += rt_fidelity/(1-rt_fidelity)
            average_route_QBER = route_SNR / (len(route) - 1)
            r_average_route_SNR += average_route_QBER
        return r_average_route_SNR / SNR_number

def SophonFixed_QPER_2(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
                action = [2, 2, 2, 2, 2]
                if p == 0:
                    all_agent_action[agent_id] = [action]
                else:
                    all_agent_action[agent_id].append(action)

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action, candidate_routes, completed_parts)
        # obtain the link-level fidelity and transmission dimension
        QPER_number = 0
        r_average_route_QPER = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            QPER_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_QPER = 0
            for rt in range(len(route) - 1):
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt] - 1][route[rt + 1] - 1]))
                rt_fidelity = 1 / math.sqrt(2) * QNConfig.p * math.pow((1 - QNConfig.p), 2 - 1) * P_rke
                if 4 - 4 * 2 * (1 - rt_fidelity) < 0:
                    route_QPER += 0.5 - rt_fidelity
                else:
                    route_QPER += (2 - math.sqrt(4 - 4 * 2 * (1 - rt_fidelity))) / 4
            average_route_QPER = route_QPER / (len(route) - 1)
            r_average_route_QPER += average_route_QPER
        return r_average_route_QPER / QPER_number

def SophonFixed_QPER_flexible(requests, data_volumes, candidate_routes, completed_requests_num,
                fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    parts = int(len(requests) / QNConfig.request_pool_len)
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
        # obtain the link-level fidelity and transmission dimension
        QPER_number = 0
        r_average_route_QPER = 0
        for r in range(len(requests)):
            if 1 not in Y[r]:
                continue
            QPER_number += 1
            route = candidate_routes[r][Y[r].index(1)]
            route_QPER = 0
            for rt in range(len(route)-1):
                node = route[rt]-1
                P_rke = math.exp(-1 * QNConfig.gamma * (QNModel.LINK_LENS[route[rt]-1][route[rt+1]-1]))
                rt_data = all_agent_action[node][int(r/QNConfig.request_pool_len)][r%QNConfig.request_pool_len]
                if rt_data == 0:
                    route_QPER += 0.5
                else:
                    rt_fidelity = 1/math.sqrt(rt_data+1) * QNConfig.p * math.pow((1-QNConfig.p), rt_data+1-1) * P_rke
                    if rt_data == 1:
                        if 4 - 4 * 2 * (1 - rt_fidelity) < 0:
                            route_QPER += 1/(rt_data+1) - rt_fidelity
                        else:
                            route_QPER += (2 - math.sqrt(4 - 4 * 2 * (1 - rt_fidelity))) / 4
                    else:
                        if 9 - 4 * 3 * (1 - rt_fidelity) < 0:
                            route_QPER += 1/(rt_data+1) - rt_fidelity
                        else:
                            route_QPER += (3 - math.sqrt(9 - 4 * 3 * (1 - rt_fidelity))) / 6
            average_route_QPER = route_QPER/(len(route)-1)
            r_average_route_QPER += average_route_QPER
        return r_average_route_QPER/QPER_number
