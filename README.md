# Sophon
An online transmission framework for high-dimensional entanglement in quantum networks.  

Python implementations of Sophon, including Sophon's training process, the deployed Sophon that compared with the baselines, the roubstness verification of Sophon.   

**Sophon contains two parts: train and deployment**, the following USER MANUAL demonstrates the details of these two aspects.

## Requirements
- [python 3.8](https://www.python.org/downloads/release/python-380/)
- [gurobi](https://www.gurobi.com/downloads/request-an-evaluation-license/?utm_source=google&utm_medium=cpc&utm_campaign=2024+na+googleads+request+an+evaluation+license&campaignid=193283256&adgroupid=51266130904&creative=601650357807&keyword=gurobipy&matchtype=e&_bn=g&gad_source=1&gclid=Cj0KCQjwq_G1BhCSARIsACc7NxofDNZjgmZVqlw7PuCsPqacAqqLqt7vJC24x2u_CyN4yM7LUmwxRHsaAt9KEALw_wcB)

```shell
$ pip install -r requirements.txt
```

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
## Quick Start (Deployment)
We can run the deployment of Sophon by
```shell
$ python ./Comparison/main_compare.py
```

## Code Roadmap

The following file diagram depicts an outline of the code, with explanations
regarding key modules in our code. 

```
Sophon
└───documentation (includes some figures from the paper)   
└───results (where local results are stored)   
└───scripts (runnable scripts that are described above)  
└───src (main code folder)
│   └───config (configuration files described above)
│   └───envs (used environments, includes multi_cart (Coupled Multi Cart Pole), multi_particle (Bounded Cooperative Navigation), payoff_matrix....
│   └───reward_decomposition (includes the full implementation for our RD method)
│   └───learners (the main learning loop, bellman updates)
│   │   │   q_learner (a modified q_learner that supports local rewards and rweard decomposition)
│   │   │   ...
│   └───modules (NN module specifications)
│   │   └───mixers (Mixing layers specifications)
│   │   │   │   gcn (a GCN implementation for LOMAQ, occasionly used)
│   │   │   │   lomaq.py (The main specification of our mixing networks)
│   │   │   │   ...
│   └───controllers (controls a set of agent utlity networks)
│   │   │   hetro_controller.py (an agent controller that doesn't implement parameter sharing)
│   │   │   ...
│   └───components (general components for LOMAQ)
│   │   │   locality_graph.py (A module that efficiently represents the graph of agents)
│   │   │   ...
│   │   main.py (for running a certain env-alg pair with default parameters)
│   │   multi_main.py (for running a certain test with multiple runs)
│   │   single_main.py (for running arun within a test)
│   │   offline_plot.py (for plotting results)
│   │   ...
│   README.md (you are here)
│   requirements.txt (all the necessary packages for running the code)



