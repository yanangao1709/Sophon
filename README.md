# Sophon
An online transmission framework for high-dimensional entanglement in quantum networks.  

**Sophon contains two parts: training and deploying**, so the following USER MANUAL demonstrates the details of these two aspects.

## Topology
**(1)** The topology is self-made, and the data is in the file *"./Topology/topology.csv"*.    
**(2)** The topology image is in the file *"./Topology/Topology.png"*.

## Initial preparation
**(1)** The initial request set is in the file *"./QNEnv/QNModel.py"*.  
**(2)** We can generate the candidate route set, the route length, and the hop number of a route for each request by executing the codes in *"./Topology/RouteGenerator.py"*.  
**(3)** After obtaining the candidate route sets, etc., comment on the codes in case of repeated calculation.  

## Train
We can train Sophon by 
```shell
$ python main.py
```



