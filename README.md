# Sophon
An online transmission framework for high-dimensional entanglement in quantum networks.  

**Sophon contains two parts: training and deploying**, so the following USER MANUAL demonstrates the details of these two aspects.

## Topology
The topology is self-made as the following:
<div align="center">
  <img src="https://github.com/yanangao1709/Sophon/blob/main/Topology/Topology.png">
</div>


# prepare initial request sets and generate candidate route sets
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
After obtaining the candidate route sets, comment on the above codes in case the repeated execution.

