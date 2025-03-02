from Config import QNConfig
from Provisioning import Agent
from QNEnv import QNModel
from Comparison.SophonDeploy.Flexible import LocalEnvFlexible, GlobalEnvFlexible, ILPFlexible
from Comparison.SophonDeploy.Flexible import QNTopologyModelFlexible
import numpy as np
import datetime

def generate_gaussian_random_numbers(mu, sigma, request_num, min_value=10, max_value=35):
    assert sigma * 3 < (max_value - min_value) / 2
    random_numbers = np.random.normal(mu, sigma, request_num)
    result = np.clip(random_numbers, min_value, max_value)
    results = []
    for r in result:
        results.append(int(r))
    return results

# 加载已经训练好的分布式代理，由于代理的规模限制，
def SophonFlexible(completed_requests_num, mu=1, sigma=0, heterogeneous = False,
                   fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    time_cost = 0
    r_success_counter = 0
    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    for agent_id in range(QNConfig.agent_num):
        local_env = LocalEnvFlexible.LocalEnv(agent_id)
        all_agent_envs[agent_id] = local_env
        all_agent_obs[agent_id] = local_env.reset()

    # 每个episode初始化一个全局环境和一个传输过程
    d_volumes = generate_gaussian_random_numbers(mu, sigma, QNConfig.request_pool_len, min_value=10, max_value=20)
    global_env = GlobalEnvFlexible.GlobalEnv(d_volumes)
    trans = ILPFlexible.Transmission(fidelity_threshold, delay_threshold)

    step = 0
    while True:
        all_agent_action = {}
        for agent_id in range(QNConfig.agent_num):
            agent = agents[agent_id]
            action = agent.get_action(all_agent_obs[agent_id])
            all_agent_action[agent_id] = action

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action)
        # 全局环境更新
        r_success_counter, current_topology = global_env.update(all_agent_envs, all_agent_action, Y, step, mu, sigma, heterogeneous)
        if r_success_counter != 0:
            trans.set_new_topology(current_topology)
        # 局部环境更新
        for agent_id in range(QNConfig.agent_num):
            next_obs = all_agent_envs[agent_id].update(current_topology)
            all_agent_obs[agent_id] = next_obs

        step += 1
        time_cost += 1
        # print(r_success_counter)
        if r_success_counter >= completed_requests_num:
            break
    return time_cost

def SophonFlexible_time(completed_requests_num, mu=1, sigma=0, heterogeneous = False,
                   fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    time_cost = 0
    r_success_counter = 0
    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    for agent_id in range(QNConfig.agent_num):
        local_env = LocalEnvFlexible.LocalEnv(agent_id)
        all_agent_envs[agent_id] = local_env
        all_agent_obs[agent_id] = local_env.reset()

    # 每个episode初始化一个全局环境和一个传输过程
    d_volumes = generate_gaussian_random_numbers(mu, sigma, QNConfig.request_pool_len, min_value=10, max_value=20)
    global_env = GlobalEnvFlexible.GlobalEnv(d_volumes)
    trans = ILPFlexible.Transmission(fidelity_threshold, delay_threshold)


    start_time = datetime.datetime.now().timestamp()
    step = 0
    all_agent_action = {}
    for agent_id in range(QNConfig.agent_num):
        agent = agents[agent_id]
        action = agent.get_action(all_agent_obs[agent_id])
        all_agent_action[agent_id] = action

    # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
    Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action)
    # 全局环境更新
    r_success_counter, current_topology = global_env.update(all_agent_envs, all_agent_action, Y, step, mu, sigma,
                                                            heterogeneous)
    end_time = datetime.datetime.now().timestamp()
    one_time = end_time - start_time

    return one_time

def SophonFlexible_computing_threshold(completed_requests_num, computing_threshold, mu=1, sigma=0, heterogeneous = False,
                   fidelity_threshold=0.00000001, delay_threshold=150):
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, True)

    time_cost = 0
    r_success_counter = 0
    # 初始化全局和局部环境
    all_agent_envs = {}
    all_agent_obs = {}
    # 为各分布式智能体建立环境
    for agent_id in range(QNConfig.agent_num):
        local_env = LocalEnvFlexible.LocalEnv(agent_id)
        all_agent_envs[agent_id] = local_env
        all_agent_obs[agent_id] = local_env.reset()

    # 每个episode初始化一个全局环境和一个传输过程
    d_volumes = generate_gaussian_random_numbers(mu, sigma, QNConfig.request_pool_len, min_value=10, max_value=20)
    global_env = GlobalEnvFlexible.GlobalEnv(d_volumes)
    trans = ILPFlexible.Transmission(fidelity_threshold, delay_threshold)

    step = 0
    start_time = datetime.datetime.now().timestamp()
    completed_request_num = 0
    while True:
        all_agent_action = {}
        for agent_id in range(QNConfig.agent_num):
            agent = agents[agent_id]
            action = agent.get_action(all_agent_obs[agent_id])
            all_agent_action[agent_id] = action

        # 进入传输阶段，聚合分割开的请求，同时为所有的请求进行全局路径选择
        Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action)
        # 全局环境更新
        r_success_counter, current_topology = global_env.update(all_agent_envs, all_agent_action, Y, step, mu, sigma,
                                                                heterogeneous)
        if r_success_counter != 0:
            trans.set_new_topology(current_topology)
        # 局部环境更新
        for agent_id in range(QNConfig.agent_num):
            next_obs = all_agent_envs[agent_id].update(current_topology)
            all_agent_obs[agent_id] = next_obs

        step += 1
        # print(r_success_counter)
        now_time = datetime.datetime.now().timestamp()
        if now_time-start_time > computing_threshold:
            if r_success_counter < completed_requests_num:
                completed_request_num = r_success_counter
            else:
                completed_request_num = completed_requests_num
            break
    return completed_request_num