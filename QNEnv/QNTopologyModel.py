# quantum network 网络模型用于管理拓扑信息、请求池、请求信息等
# 该网络模型是动态的，随着请求被成功响应，请求池被更新，伴随着涉及的拓扑信息被更新
from Config import QNConfig
import random
from Topology import RouteGenerator

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
        s_r = random.randint(0, QNConfig.node_num)
        if s_r != QNConfig.node_num:
            s_r += 1
        d_r = random.randint(0, QNConfig.node_num)
        if d_r != QNConfig.node_num:
            d_r += 1
        if s_r == d_r:
            s_r = 1
            d_r = 11
        return [s_r, d_r]

    def update_request_pool_and_topology_info(self, r_state, exec = False):
        # 更新拓扑包括更新：路径集ROUTES更新、路径长度ROUTES_LEN更新、路径经过节点信息H_RKN更新、路径跳数ROUTES_HOPS更新
        pop_index = []
        remaining_r = []
        for r in range(QNConfig.request_pool_len):
            if r_state[r]:  # 被成功完成响应
                pop_index.append(r)
            else:
                remaining_r.append(r)
        self.pop_r(pop_index)
        self.append_r(len(pop_index), exec)

    def pop_r(self, pop_index):
        self.REQUESTSET = [self.REQUESTSET[i] for i in range(len(self.REQUESTSET)) if i not in pop_index]
        self.D_VOLUMN = [self.D_VOLUMN[i] for i in range(len(self.D_VOLUMN)) if i not in pop_index]
        self.ROUTES = [self.ROUTES[i] for i in range(len(self.ROUTES)) if i not in pop_index]
        self.ROUTES_LEN = [self.ROUTES_LEN[i] for i in range(len(self.ROUTES_LEN)) if i not in pop_index]
        self.H_RKN = [self.H_RKN[i] for i in range(len(self.H_RKN)) if i not in pop_index]
        self.ROUTES_HOPS = [self.ROUTES_HOPS[i] for i in range(len(self.ROUTES_HOPS)) if i not in pop_index]

    def append_r(self, new_r_num, exec = False):
        for new_r in range(new_r_num):
            # -------(1)原始Sophon训练;(2)不固定请求个数实验-------
            new_r = self.generate_a_request()
            self.D_VOLUMN.append(random.randint(QNConfig.volume_lower, QNConfig.volume_upper))
            # --------------------------------------------

            self.REQUESTSET.append(new_r)
            routes_info = RouteGenerator.generate_routes(new_r, exec)
            self.ROUTES.append(routes_info[1])
            self.ROUTES_LEN.append(routes_info[0])
            self.update_H_RKN(routes_info[1])
            self.upadate_ROUTES_HOPS(routes_info[1])

    def update_H_RKN(self, new_routes):
        h_rkn = [[0] * QNConfig.node_num for i in range(QNConfig.candidate_route_num)]
        for rt in range(QNConfig.candidate_route_num):
            route = new_routes[rt]
            for node in range(QNConfig.node_num):
                if node+1 in route:
                    h_rkn[rt][node] = 1
        self.H_RKN.append(h_rkn)

    def upadate_ROUTES_HOPS(self, new_routes):
        hops = [0 for i in range(QNConfig.candidate_route_num)]
        for rt in range(QNConfig.candidate_route_num):
            route = new_routes[rt]
            hops[rt] = len(route)
        self.ROUTES_HOPS.append(hops)






