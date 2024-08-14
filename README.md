# Sophon
An online transmission framework for high-dimensional entanglement in quantum networks.  

Pytorch implementations of Sophon, including the training process and the execution of Sophon with the comparison methods.   

**Sophon contains two parts: training and deploying**, so the following USER MANUAL demonstrates the details of these two aspects.

## Requirements
- python
- torch
- [gurobi](https://www.gurobi.com/downloads/request-an-evaluation-license/?utm_source=google&utm_medium=cpc&utm_campaign=2024+na+googleads+request+an+evaluation+license&campaignid=193283256&adgroupid=51266130904&creative=601650357807&keyword=gurobipy&matchtype=e&_bn=g&gad_source=1&gclid=Cj0KCQjwq_G1BhCSARIsACc7NxofDNZjgmZVqlw7PuCsPqacAqqLqt7vJC24x2u_CyN4yM7LUmwxRHsaAt9KEALw_wcB)

## Topology
**(1)** The topology is self-made, and the data is in the file *"./Topology/topology.csv"*.    
**(2)** The topology image is in the file *"./Topology/Topology.png"*.

## Initial preparation
**(1)** The initial request set is in the file *"./QNEnv/QNModel.py"*.  
**(2)** We can generate the candidate route set, the route length, and the hop number of a route for each request by executing the codes in *"./Topology/RouteGenerator.py"*.  
**(3)** After obtaining the candidate route sets, etc., comment on the codes in case of repeated calculation.  

## Quick Start (Train)
We can train Sophon by 
```shell
$ python main.py
```



