# 拓扑可视化、给请求对求取前k最短路径
import pandas as pd
import networkx as nx
import os
from Topology import k_shortest_paths
from Config import QNConfig
from QNEnv.QNModel import REQUESTSET
import matplotlib.pyplot as plt

topology_myself_data_path = "D:\\Python\\Sophon\\Topology\\topology.csv"
edge_length = {}

# -------------------------------绘制拓扑-------------------------------
def draw(data_path):
    nodes_num = 18
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
        topology_file_path = os.getcwd() + "\\..\\Topology\\topology.csv"
    else:
        topology_file_path = topology_myself_data_path
    G = draw(topology_file_path)
    routes_info = k_shortest_paths.k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
    return routes_info


# -----------------------------------为请求集REQUESTSET中的请求对生成候选路径------------------------------------------------
# G = draw(topology_myself_data_path)
# ROUTES = []
# ROUTES_LEN = []
# ROUTES_HOPS = []
# for r in REQUESTSET:
#     routes_len, r_routes = k_shortest_paths.k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
#     ROUTES.append(r_routes)
#     ROUTES_LEN.append(routes_len)
#     ROUTES_HOPS.append([len(route) for route in r_routes])
# print(ROUTES)
# print(ROUTES_LEN)
# print(ROUTES_HOPS)