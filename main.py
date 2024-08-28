# 主程序入口
# 初始化网络
# 运行provisioning stage + transmitting stage
# 运行provisioning stage 的阶段有两个：训练和加载训练好的模型
from Config import QNConfig, AgentConfig
from Provisioning import Agent
import numpy as np
from QNEnv import LocalQN, GlobalQN
from Transmitting import ILP
import torch
import pylab
import sys
import matplotlib as plt
import pandas as pd


def run():
    # 初始化各个智能体代理
    agents = {}
    for agent_id in range(QNConfig.agent_num):
        agents[agent_id] = Agent.Agent(agent_id, False)

    total_step = 0
    global_rewards = []
    episodes = []
    suc_datas = []
    max_ILP_objs = []
    agent_local_rewards = {}
    agent_memory_usage = {}
    for agent in range(QNConfig.node_num):
        agent_local_rewards[agent] = [0 for sp in range(AgentConfig.episodes_length + 1)]
        agent_memory_usage[agent] = [0 for sp in range(AgentConfig.episodes_length + 1)]
    # episode的执行，需要所有智能体配合完成
    for ep in range(AgentConfig.episodes_length + 1):
        all_agent_envs = {}
        all_agent_obs = {}
        # 为各分布式智能体建立环境
        for agent_id in range(QNConfig.agent_num):
            local_env = LocalQN.LocalQN(agent_id)
            all_agent_envs[agent_id] = local_env
            all_agent_obs[agent_id] = local_env.reset()
        # 每个episode初始化一个全局环境和一个传输过程
        global_env = GlobalQN.GlobalQN()
        trans = ILP.Transmission()
        done = False
        score = 0
        sum_max_ILP_obj = 0
        suc_data_ep = 0
        step = 0
        while not done:
            all_agent_action = {}
            for agent_id in range(QNConfig.agent_num):
                agent = agents[agent_id]
                action = agent.get_action(all_agent_obs[agent_id])
                all_agent_action[agent_id] = action
            # 进入传输阶段，选择路径
            Y, max_ILP_obj = trans.transmit(all_agent_envs, all_agent_action)
            # 依据选择的路径，完成传输，全局网络状态更新
            global_reward, done, current_topology, success_data = global_env.step(all_agent_envs, all_agent_action, Y,
                                                                                  step)
            if global_reward != 0:
                trans.set_new_topology(current_topology)
            # 分布式节点局部状态更新，智能体的动作与环境交互
            for agent_id in range(QNConfig.agent_num):
                next_obs, local_reward, memory_usage = all_agent_envs[agent_id].step(all_agent_action[agent_id], global_reward,
                                                                       current_topology, Y)
                # save the sample <s, a, r, s'> to the replay memory
                agents[agent_id].append_sample(all_agent_obs[agent_id], all_agent_action[agent_id], local_reward,
                                               next_obs, done)
                # print("agent_id:" + str(agent_id) + "-------------local reward:" + str(local_reward))
                agent_local_rewards[agent_id][ep] += local_reward
                agent_memory_usage[agent_id][ep] += memory_usage
                # train
                if total_step >= AgentConfig.memory_size:
                    agents[agent_id].train_model(done, ep)
                # 我们必须区分多个奖励概念：
                # 总体奖励：每个episode中被成功响应的请求个数
                # 中心化控制平台的奖励：maximize的最大传输数据量
                # 各分布式节点的分布式奖励：local_reward
                all_agent_obs[agent_id] = next_obs
            step += 1
            total_step += 1
            score += global_reward
            suc_data_ep += success_data
            sum_max_ILP_obj += max_ILP_obj

            if done:
                # every episode update the target model to be same with model
                if ep % 10 == 0:
                    for agent_id in range(QNConfig.agent_num):
                        agents[agent_id].update_target_model()

                # every episode, plot the play time
                global_rewards.append(score)
                episodes.append(ep)
                suc_datas.append(suc_data_ep)
                max_ILP_objs.append(sum_max_ILP_obj)
                print("---------------episode:", ep, "-------------score:",
                      score, "---------------------max_objs:", sum_max_ILP_obj, "---------------------suc_data:",
                      suc_data_ep)

                # stop training
                if ep % 1000 == 0:
                    for agent_id in range(QNConfig.agent_num):
                        torch.save(agents[agent_id].model.state_dict(),
                                   "./save_model/node_agent_" + str(agent_id) + ".pth")
        if ep % 1000 == 0:
            draw_episode = {"episode": [i for i in range(len(global_rewards))], "episode_rewards": global_rewards,
                            "max_obj": max_ILP_objs, "suc_datas": suc_datas}
            pd.DataFrame(draw_episode).to_csv('./save_graph/global_rewards.csv', index=False)
            pd.DataFrame(agent_local_rewards).to_csv('./save_graph/agent_local_rewards.csv', index=False)
            pd.DataFrame(agent_memory_usage).to_csv('./save_graph/agent_memory_usage.csv', index=False)


if __name__ == '__main__':
    # -------------------train------------------------
    for i in range(1):
        run()

