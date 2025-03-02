from Comparison.AlternativeTechniques.EFiRAP import *
import datetime

def EFiRAP_com(requests, data_volumes, candidate_routes):
    new_requests = requests.copy()
    new_node_capacity = QNModel.NODE_CPA.copy()
    new_data_volumes = data_volumes.copy()
    allocated_r_rt_data_one_time = runEFiRAP_com(new_requests, candidate_routes, new_node_capacity)
    accumulated_completed_r_route_allocated = [[0 for rt in range(QNConfig.candidate_route_num)] for r in range(len(new_requests))]

    com_cost = 0
    flag = False
    while not flag:
        completed_r_data = [0 for r in range(len(new_requests))]
        for r in range(len(new_requests)):
            accumulated_completed_r_route_allocated[r] = [a + b for a, b in zip(accumulated_completed_r_route_allocated[r], allocated_r_rt_data_one_time[r])]
            completed_r_data[r] = sum(accumulated_completed_r_route_allocated[r])
        flag = all(a <= b for a, b in zip(new_data_volumes, completed_r_data))
        if not flag:
            new_new_requests = []
            new_candidate_routes = []
            new_new_data_volumes = []
            new_accumulated_completed_r_route_allocated = []
            for r in range(len(new_requests)):
                if completed_r_data[r] < new_data_volumes[r]:
                    # 请求没有被完全响应，所以持续占据资源
                    for rt in range(QNConfig.candidate_route_num):
                        route = candidate_routes[r][rt]
                        for n in route:
                            new_node_capacity[n-1] -=  allocated_r_rt_data_one_time[r][rt]
                    new_new_requests.append(new_requests[r])
                    new_candidate_routes.append(candidate_routes[r])
                    new_new_data_volumes.append(new_data_volumes[r])
                    new_accumulated_completed_r_route_allocated.append(accumulated_completed_r_route_allocated[r])
                else:
                    # 请求被完全响应，释放所有累积占据的资源
                    for rt in range(QNConfig.candidate_route_num):
                        route = candidate_routes[r][rt]
                        for n in route:
                            if new_node_capacity[n - 1] < QNModel.NODE_CPA[n - 1]:
                                new_node_capacity[n-1] +=  accumulated_completed_r_route_allocated[r][rt]

            allocated_r_rt_data_one_time = runEFiRAP_com(new_new_requests, new_candidate_routes, new_node_capacity)

            new_data_volumes.clear()
            new_data_volumes = [ dv for dv in new_new_data_volumes]
            new_requests.clear()
            new_requests = [nr for nr in new_new_requests]

            if any(x < 2 for x in new_node_capacity):
                new_node_capacity.clear()
                new_node_capacity = QNModel.NODE_CPA.copy()
                accumulated_completed_r_route_allocated.clear()
                accumulated_completed_r_route_allocated = [[0 for rt in range(QNConfig.candidate_route_num)] for r in range(len(new_requests))]
            else:
                accumulated_completed_r_route_allocated.clear()
                accumulated_completed_r_route_allocated = [nacr for nacr in new_accumulated_completed_r_route_allocated]

        com_cost += 1
    return com_cost

def EFiRAP_time(requests, data_volumes, candidate_routes):
    new_requests = requests.copy()
    new_node_capacity = QNModel.NODE_CPA.copy()

    start_time = datetime.datetime.now().timestamp()
    allocated_r_rt_data_one_time = runEFiRAP_com(new_requests, candidate_routes, new_node_capacity)
    end_time = datetime.datetime.now().timestamp()
    one_time = end_time - start_time

    return one_time