# quantum network 网络模型用于管理拓扑信息、请求池、请求信息等
# 该网络模型是动态的，随着请求被成功响应，请求池被更新，伴随着涉及的拓扑信息被更新
from Config import QNConfig
import random
from Topology import RouteGenerator
import numpy as np

class QNModel():
    def __init__(self, request_set, d_volume, routes, routes_len, H_RKN, routes_hops, node_cap):
        self.REQUESTSET = request_set
        self.D_VOLUMN = d_volume
        self.ROUTES = routes
        self.ROUTES_LEN = routes_len
        self.H_RKN = H_RKN
        self.ROUTES_HOPS = routes_hops
        self.Capacity_nodes = node_cap

    def generate_a_request(self):
        return random.sample(range(1, QNConfig.node_num), 2)

    def update_request_pool_and_topology_info(self, r_state, exec = False, mu=1, sigma=0, heterogeneous = False):
        # 更新拓扑包括更新：路径集ROUTES更新、路径长度ROUTES_LEN更新、路径经过节点信息H_RKN更新、路径跳数ROUTES_HOPS更新
        pop_index = []
        for r in range(QNConfig.request_pool_len):
            if r_state[r]:  # 被成功完成响应
                pop_index.append(r)
                if heterogeneous:
                    # 异质性请求实验，调整正态分布参数
                    assert sigma * 3 < (QNConfig.volume_upper - QNConfig.volume_lower) / 2
                    random_numbers = np.random.normal(mu, sigma, 1)
                    result = np.clip(random_numbers, QNConfig.volume_lower, QNConfig.volume_upper)
                    new_r = self.generate_a_request()
                    routes_info = RouteGenerator.generate_routes(new_r, exec)
                    while (routes_info is None) or (len(routes_info[1]) != QNConfig.candidate_route_num):
                        new_r = self.generate_a_request()
                        routes_info = RouteGenerator.generate_routes(new_r, exec)
                    self.REQUESTSET[r] = new_r
                    self.D_VOLUMN[r] = (int(result))
                else:
                    new_r = self.generate_a_request()
                    routes_info = RouteGenerator.generate_routes(new_r, exec)
                    while (routes_info is None) or (len(routes_info[1]) != QNConfig.candidate_route_num):
                        new_r = self.generate_a_request()
                        routes_info = RouteGenerator.generate_routes(new_r, exec)
                    self.REQUESTSET[r] = new_r
                    self.D_VOLUMN[r] = random.randint(QNConfig.volume_lower, QNConfig.volume_upper)
                self.ROUTES[r] = routes_info[1]
                self.ROUTES_LEN[r] = routes_info[0]
                self.update_H_RKN(r, routes_info[1])
                self.upadate_ROUTES_HOPS(r, routes_info[1])

    def update_H_RKN(self, r, new_routes):
        h_rkn = [[0] * QNConfig.node_num for i in range(QNConfig.candidate_route_num)]
        for rt in range(QNConfig.candidate_route_num):
            route = new_routes[rt]
            for node in range(QNConfig.node_num):
                if node+1 in route:
                    h_rkn[rt][node] = 1
        self.H_RKN[r] = h_rkn

    def upadate_ROUTES_HOPS(self, r, new_routes):
        hops = [0 for i in range(QNConfig.candidate_route_num)]
        for rt in range(QNConfig.candidate_route_num):
            route = new_routes[rt]
            hops[rt] = len(route)
        self.ROUTES_HOPS[r] = hops






