# 拓扑可视化、给请求对求取前k最短路径
import pandas as pd
import networkx as nx
import os
from Topology import k_shortest_paths
from Config import QNConfig

topology_myself_data_path = os.getcwd() + "./Topology/topology.csv"
edge_length = {}

def draw():
    nodes_num = 18
    nodes = [i + 1 for i in range(nodes_num)]
    data = pd.read_csv(topology_myself_data_path)
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    node1 = data["node1"].values.tolist()
    node2 = data["node2"].values.tolist()
    length = data["length"].values.tolist()
    for i in range(len(node1)):
        G.add_edge(node1[i], node2[i], length=length[i])
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

def generate_routes(r):
    G = draw()
    routes_info = k_shortest_paths.k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
    return routes_info

# route_generation(r)
# G = draw()
# ROUTES = []
# ROUTES_LEN = []
# ROUTES_HOPS = []
# for r in REQUESTSET:
#     routes_len, r_routes = k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
#     ROUTES.append(r_routes)
#     ROUTES_LEN.append(routes_len)
#     ROUTES_HOPS.append([len(route) for route in r_routes])
# print(ROUTES)
# print(ROUTES_LEN)
# print(ROUTES_HOPS)

# print(k_shortest_paths(G, 12, 6, 6, weight=customed_weight))
