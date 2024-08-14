# Sophon
An online transmission framework for high-dimensional entanglement in quantum networks.  

**Sophon contains two parts: training and deploying**, so the following USER MANUAL demonstrates the details of these two aspects.

## Topology
(1) The topology is self-made, and the data is in the file *"./Topology/topology.csv"*.    
(2) The topology image is in the file *"./Topology/Topology.png"*.

## Initial preparation
(1) The initial request set is in the file *"./QNEnv/QNModel.py"*.  
(2) We can generate the candidate route set, the route length, and the hop number of a route for each request by executing the codes in *"./Topology/RouteGenerator.py"*.  
(3) After obtaining the candidate route sets, etc., comment on the codes in case of repeated calculation.  

"./QNEnv/QNModel.py"  stores the initial topology and requests information. We can execute "./Topology/RouteGenerator.py" to generate each request's candidate route sets, route_len, and route_hop. The codes are:
```shell
G = draw(topology_myself_data_path)
ROUTES = []
ROUTES_LEN = []
ROUTES_HOPS = []
for r in REQUESTSET:
    routes_len, r_routes = k_shortest_paths.k_shortest_paths(G, r[0], r[1], QNConfig.candidate_route_num, weight=customed_weight)
    ROUTES.append(r_routes)
    ROUTES_LEN.append(routes_len)
    ROUTES_HOPS.append([len(route) for route in r_routes])
print(ROUTES)
print(ROUTES_LEN)
print(ROUTES_HOPS)
'''


