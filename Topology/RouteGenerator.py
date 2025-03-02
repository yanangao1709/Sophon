# 拓扑可视化、给请求对求取前k最短路径
import random

import pandas as pd
import numpy as np
import networkx as nx
import os
from Topology import k_shortest_paths
from Config import QNConfig
import matplotlib.pyplot as plt

topology_myself_data_path = "D:\\Python\\Sophon\\Topology\\topology.csv"
edge_length = {}

# -------------------------------绘制拓扑-------------------------------
def draw(data_path):
    nodes_num = QNConfig.node_num
    nodes = [i + 1 for i in range(nodes_num)]
    data = pd.read_csv(data_path)
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    node1 = data["node1"].values.tolist()
    node2 = data["node2"].values.tolist()
    length = data["length"].values.tolist()
    for i in range(len(node1)):
        G.add_edge(node1[i], node2[i], length=length[i])

    # 显示拓扑
    # nx.draw(G, pos=nx.spring_layout(G), with_labels=True, node_color='y')
    # plt.show()
    return G

def customed_weight(u, v, d):
    '''
    networkx single_source_dijkstra() weight function implementation
    :param u:
    :param v:
    :param d:
    :return:
    '''
    edge_wt = d.get("length", 1)
    return edge_wt

def generate_routes(r, exec = False):
    if exec:
        topology_file_path = "D:\\Python\\Sophon\\Topology\\topology.csv"
    else:
        topology_file_path = topology_myself_data_path
    G = draw(topology_file_path)
    routes_info = k_shortest_paths.k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
    return routes_info

if __name__ == '__main__':
    # -------------------------------生成请求及其路径信息-----------------------------------------
    REQUESTSET = []
    VOLUME = []
    G = draw(topology_myself_data_path)
    ROUTES = []
    ROUTES_LEN = []
    ROUTES_HOPS = []
    for r in range(20):
        request = random.sample(range(1, QNConfig.node_num), 2)
        shortest_paths = k_shortest_paths.k_shortest_paths(G, request[0], request[1], QNConfig.candidate_route_num,
                                                                 weight=customed_weight)
        while (shortest_paths == None) or (len(shortest_paths[1])!=QNConfig.candidate_route_num):
            request = random.sample(range(1, QNConfig.node_num), 2)
            shortest_paths = k_shortest_paths.k_shortest_paths(G, request[0], request[1],
                                                               QNConfig.candidate_route_num, weight=customed_weight)
        REQUESTSET.append(request)
        ROUTES.append(shortest_paths[1])
        ROUTES_LEN.append(shortest_paths[0])
        ROUTES_HOPS.append([len(route) for route in shortest_paths[1]])
        VOLUME.append(random.randint(QNConfig.volume_lower, QNConfig.volume_upper))
    print(REQUESTSET)
    print(VOLUME)
    print(ROUTES)
    print(ROUTES_LEN)
    print(ROUTES_HOPS)

    # ---------------------------------为不同规模的QNModel生成LINK_LENS--------------------------------------------------------
    topology = pd.read_csv(topology_myself_data_path)
    LINK_LENS = [[0 for j in range(QNConfig.node_num)] for i in range(QNConfig.node_num)]
    for index, row in topology.iterrows():
        LINK_LENS[int(row['node1'])-1][int(row['node2'])-1] = row['length']
        LINK_LENS[int(row['node2'])-1][int(row['node1'])-1] = row['length']
    print(LINK_LENS)

    # --------------------------------用高斯分布在[9,26]之间生成随机数，用作node memory capacity----------------------------------
    NODE_CPA = []
    for n in range(QNConfig.node_num):
        NODE_CPA.append(int(random.uniform(9, 26)))
    print(NODE_CPA)

    H_RKN = [[[0] * QNConfig.node_num for i in range(QNConfig.candidate_route_num)] for j in range(len(REQUESTSET))]
    for r in range(len(REQUESTSET)):
        for k,p in enumerate(ROUTES[r]):
            for n in range(len(p)):
                H_RKN[r][k][p[n]-1] = 1
    print(H_RKN)
