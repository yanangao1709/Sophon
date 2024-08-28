
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     Author: Yanan Gao                                       #
#       Date: 04-08-2023                                      #
#      Goals: implement the quantum network environment       #
#             for request response                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from Topology.RouteGenerator import ROUTES, HOPS, NODE_CPA, D_VOLUMN, H_RKN
import numpy as np
import torch as th
from ResourceAllocation.components.locality_graph import DependencyGraph
import networkx as nx
import pandas as pd

class QuantumNetwork:
    def __init__(self):
        self.requests = None
        self.agent_local_env = []
        self.node_cap = None
        self.H_RKN = np.zeros((tohp.request_num, tohp.nodes_num))

        self.episode_limit = RLhp.EPISODE_LIMIT
        self.episode_steps = 0
        self.request_num = tohp.request_num
        self.obs_size = 3 * tohp.request_num + tohp.request_num + 1   # 6 9 7 5
        self.state_size = 18
        self.episode_steps = 0
        self.reward_shape = tohp.nodes_num
        self.n_actions = RLhp.NUM_ACTIONS
        self.n_agents = tohp.nodes_num

        self.graph_obj = self.build_graph()
        self.T_r = [20 for i in range(tohp.request_num)]
        self.requests = [[1,11], [2,13], [3,14], [2,9], [7,18]]
        self.d_volume = [120, 120, 120, 120, 120]

    def obtain_requests(self):
        rg = rrg.RequestAndRouteGeneration()
        requests = rg.request_routes_generation()
        return requests

    def get_H_RKN(self):
        return self.H_RKN

    def reset(self):
        self.episode_steps = 0
        # if self.requests:
            # self.requests.clear()
        # self.requests = self.obtain_requests()
        # self.requests = REQUESTSET
        # self.obtain_H_RKN()
        self.node_cap = NODE_CPA
        # random photon allocation
        photonallocated = [
            [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 3, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 0, 2]
        ]
        # photonallocated2 = [
        #     [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 3, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 0, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 3, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 0, 2]
        # ]
        # photonallocated2 = [
        #     [2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2],
        #     [2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        # ]
        selected_route = [[0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
        # selected_route2 = [[0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1]]
        # selected_route2 = [[0, 0, 1], [1, 0, 0], [0, 0, 1], [0, 0, 1]]
        return photonallocated, selected_route

    def get_state(self):
        # 节点内存信息 size = 18
        return np.array(self.node_cap)

    def get_avail_actions(self):
        avail_actions = []
        for i in range(tohp.nodes_num):
            actions = np.ones((tohp.request_num, RLhp.NUM_ACTIONS))
            avail_actions.append(actions)
        return avail_actions

    def get_obs(self):
        # request information, route information, capacity information
        ob = np.zeros([tohp.nodes_num, self.obs_size])
        for i in range(tohp.nodes_num):
            obs = []
            for r in range(len(self.requests)):
                obs.append(self.requests[r][0])
                obs.append(self.requests[r][1])
                obs.append(self.d_volume[r])
            for j in range(tohp.request_num):
                obs.append(self.H_RKN[j][i])
                # 固定路径时，用local节点的内存
                # obs.append(self.node_cap[i])
            obs.append(self.node_cap[i])
            ob[i, :] = obs
        return ob

    def setSelectedRoutes(self, selectedroutes):
        for r in range(tohp.request_num):
            route = ROUTES[r][selectedroutes[r].index(1)]
            for m in range(tohp.nodes_num):
                if m+1 in route:
                    self.H_RKN[r][m] = 1

    def obtain_Tr(self, ps, t):
        z = 20
        T_r_t = [20 for i in range(tohp.request_num)]
        for r in range(tohp.request_num):
            z_r = 0
            data_volume = 0
            for ep in range(t):
                for k in range(tohp.candidate_route_num):
                    data_volume_k = 0
                    if ps.Y_his[ep][r][k]:
                        for m in range(tohp.nodes_num):
                            data_volume_k += ps.Y_his[ep][r][k] * ps.M_his[ep][r][m]
                        data_volume += data_volume_k * (1 / HOPS[r][k])
                if data_volume > D_VOLUMN[r]:
                    z_r = ep
                    break
            if z_r != 0 and z == 100:
                z = 0
            z += z_r
            T_r_t[r] = z
        return T_r_t

    def compute_all_rewards(self, actions, ps):
        T_r_t_1 = self.obtain_Tr(ps, self.episode_steps-1)
        T_r_t = self.obtain_Tr(ps, self.episode_steps)
        rewards = np.zeros((tohp.nodes_num,))
        for m in range(tohp.nodes_num):
            for r in range(tohp.request_num):
                if T_r_t[r] < T_r_t_1[r]:
                    y_his = ps.get_Y_his[self.episode_steps][r]
                    r_route = y_his.index(1)
                    if actions[m][r] > 0:
                        rewards[m,] += 50
                    elif H_RKN[r][r_route][m] == 1 and actions[m][r] <= 0:
                        rewards[m,] -= 50
                else:
                    if actions[m][r] > 0:
                        rewards[m,] += 20
            # rewards[i,] += sum(actions[i])
            if self.node_cap[m] < 0:
                rewards[m,] -= 10

        return rewards

    def step(self, actions, ps):
        if th.is_tensor(actions):
            actions = actions.cpu().detach().numpy().tolist()
        else:
            actions = actions.tolist()
        self.episode_steps += 1
        # we now need to compute the global reward
        rewards = self.compute_all_rewards(actions, ps)
        total_rewards = self.obtain_Tr(ps, self.episode_steps)

        # set action for each agent
        for agent in range(tohp.nodes_num):
            self._set_action(actions[agent], agent)

        # check if times up, and return done
        done = self.episode_steps >= self.episode_limit

        # next_states, reward, global_reward = self.transmit(actions)

        return rewards, sum(total_rewards)/tohp.request_num, done, {}

    def _set_action(self, actions, agent):
        self.node_cap[agent] -= sum(actions)

    def generateRequestsandRoutes(self):
        rg = rrg.RequestAndRouteGeneration()
        self.requests = rg.request_routes_generation()

    def getEngState(self, i, i_cp, j, j_cp):
        state_probs = self.multi_qubit_entgle.redefine_assign_qstate_of_multiqubits(i, i_cp, j, j_cp)
        return state_probs

    def build_auto_graph(self):
        graph = nx.Graph()
        data = pd.read_csv(tohp.topology_data_path)

        # add all the agents (necessary for the empty case)
        for i in range(self.n_agents):
            graph.add_node(i)

        node1 = data["node1"].values.tolist()
        node2 = data["node2"].values.tolist()
        length = data["length"].values.tolist()
        for i in range(len(node1)):
            graph.add_edge(node1[i]-1, node2[i]-1, length=length[i])

        return graph


    def build_graph(self):
        graph = self.build_auto_graph()
        return DependencyGraph(num_agents=self.n_agents, graph=graph)

    def get_graph_obj(self):
        return self.graph_obj

    def get_env_info(self):
        env_info = {"state_shape": self.state_size,
                    "obs_shape": self.obs_size,
                    "reward_shape": self.reward_shape,
                    "n_actions": self.n_actions,
                    "n_agents": self.n_agents,
                    "request_num": self.request_num,
                    "episode_limit": self.episode_limit,
                    "graph_obj": self.get_graph_obj(),
                    }
        return env_info
