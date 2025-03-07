# Sophon
An online link-level transmission framework for multi-qubit entanglement in quantum networks.  

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
**(3)** The topology and the requests are generated according to the following steps:  
a. go to "Sophon/Topology/TopologyGenerator.py";  
b. set the variable "NUM_NODE" to determine the topology size;  
c. run the ".py" to generate the topology information in the "./Nodes/" file, and copy the "topology.csv" file to "Sophon/Topology/";  
d. create the "QNModel.py" in "Sophon/QNEnv/" for this topology;  
e. modify the parameter "node_num" in "Sophon/Config/TopologyConfig.py";  
f. run the file "Sophon/Topology/RouteGenerator.py" to obtain "REQUESTSET, D_VOLUMN, ROUTES, ROUTES_LEN, ROUTES_HOPS, LINK_LENS, NODE_CPA, H_RKN";  
g. put the outputs to "QNModel.py".



## Initial preparation
**(1)** The initial request set required for training is in the file *"./QNEnv/QNModel.py"*.  
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
└───Comparison (the comparison with baselines, including Deployment codes, Trained models, data, results, and figures)
│   └───AlternativeTechniques (The implementation of EFiRAP and Multi_R, and the comparison performance between Sophon with these alternative techniques)
│   │   └───Fixed (Fixed deployment scheme)
│   │   │   │   GlobalEnvFixed (global environment for Fixed_Sophon)
│   │   │   │   ILPFixed (brand-and-bound algorithm and LP solving for Fixed_Sophon)
│   │   │   │   LocalEnvFixed (local environment for Fixed_Sophon)
│   │   │   │   QNTopologyModelFixed (control the updating of the request pool for Fixed_Sophon)
│   │   └───Flexible (Flexible deployment scheme)
│   │   │   │   GlobalEnvFlexible (global environment for Flexible_Sophon)
│   │   │   │   ILPFlexible (brand-and-bound algorithm and LP solving for Flexible_Sophon)
│   │   │   │   LocalEnvFlexible (local environment for Flexible_Sophon)
│   │   │   │   QNTopologyModelFlexible (control the updating of the request pool for Flexible_Sophon)
│   │   main_AT (run the comparison implementation of one-time entanglement transmission to draw Fig.7(c), Fig.7(d), and Fig.8(c), Fig.8(d))
│   │   EFiRAP (the implementation of EFiRAP for one-time transmission)
│   │   Multi_R (the implementation of EFiRAP for one-time transmission)
│   │   SophonFixed_AT (the interface for returning the one-time transmission throughput and the average memory used rate)
│   │   SophonFlexible_AT (the interface for returning the one-time transmission throughput and the average memory used rate)
│   │   draw_results (draw the figures)
│   │   AMUR_topology_scale_AT.csv (The comparison performance of the average memory used rate with various topology scales)
│   │   Throughput_node_capacity_AT.csv (The comparison performance of the one-time throughput with various node memory scales)
│   │   Throughput_request_AT.csv (The comparison performance of the one-time throughput with various request scales)
│   │   Throughput_topology_scale_AT.csv (The comparison performance of the one-time throughput with various topology scales)
│   └───data (the $2000$ request data for the comparison)
│   └───QuantumBitError (The implementation and performance results of computing QBER, QPER, SNR)
│   │   └───main_QBE (call the interface to compute the average QBER, SNR, QPER)
│   │   └───SophonFixed_QBER (SophonFixed scheme computes the average QBER, SNR, and QPER, respectively, with one-qubit and multi-qubit entanglement)
│   │   └───obtainQBER (obtain the QBER equation with the enlarging entanglement dimension)
│   │   └───draw_QBE_results (draw the Fig.12)
│   │   └───AQBER_requests (the comparison performance of AQBER with various request scales)
│   │   └───AQPER_requests (the comparison performance of APBER with various request scales)
│   │   └───SNR_requests (the comparison performance of SNR with various request scales)
│   └───SophonDeploy (Sophon deployment implementation)
│   │   └───Fixed (Fixed deployment scheme)
│   │   │   │   GlobalEnvFixed (global environment for Fixed_Sophon)
│   │   │   │   ILPFixed (brand-and-bound algorithm and LP solving for Fixed_Sophon)
│   │   │   │   LocalEnvFixed (local environment for Fixed_Sophon)
│   │   │   │   QNTopologyModelFixed (control the updating of the request pool for Fixed_Sophon)
│   │   └───Flexible (Flexible deployment scheme)
│   │   │   │   GlobalEnvFlexible (global environment for Flexible_Sophon)
│   │   │   │   ILPFlexible (brand-and-bound algorithm and LP solving for Flexible_Sophon)
│   │   │   │   LocalEnvFlexible (local environment for Flexible_Sophon)
│   │   │   │   QNTopologyModelFlexible (control the updating of the request pool for Flexible_Sophon)
│   └───TrainedModel (the distributed agents saved after training is completed, respectively, with |R|=5,10,15,20 and various topology scales  ranging from 18 to 108)
│   └───results (the comparison results)
│   │   │   adjust_threshold_fidelity.csv (the results of comparing fidelity thresholds, generated by main_compare.py)
│   │   │   adjust_threshold_delay.csv (the figures comparing delay thresholds generated by main_compare.py)
│   │   │   heterogeneous_requests_mu.csv (the results of adjusting the expectations of request data volume generated by main_compare.py)
│   │   │   heterogeneous_requests_sigma.csv (the figures of adjusting the variances of request data volume, generated by main_compare.py)
│   │   │   draw1_com (draw figures)
│   │   EFiRAP_com (EFiRAP implementation of the whole process for responding to the request set)
│   │   Multi_R_com (Multi_R implementation of the whole process for responding to the request set)
│   │   SophonFixed_com (Fixed_Sophon's start of the whole process for responding to the request set)
│   │   SophonFlexible_com (Flexible_Sophon's start of the whole process for responding to the request set)
│   │   main_compare (start of the comparison performance of the whole process for responding to the request set)
└───Config (the config files of Sophon)
│   │   AgentConfig (RL agent's configs)
│   │   QNConfig (quantum network's configs)
│   │   TopologyConfig (Topology's configs)
└───Examples (example implementation)
│   │   All_in (OBO scheme's implementation)
│   │   All_in (All_in scheme's implementation)
│   │   At_most_one_route (AMOR scheme's implementation)
│   │   At_most_one_route1 (AMOR scheme's implementation with a larger solution space)
│   │   Topology_exp (example's topology model)
│   │   draw_exp (draw the figures of example)
│   │   exp_* (the example figures)
│   │   main_exp (start to run the example)
└───Provisioning (the provisioning process of distributed agents)
│   │   Agent (distributed RL agents)
│   │   MyDQN (DQN model with training process)
│   │   ExperienceMemory (storage the experience of RL agent)
└───QNEnv (quantum network environment)
│   │   GlobalQN (global environment for Sophon)
│   │   LocalQN (local environments for distributed agents)
│   │   QNModel (the network model for Sophon)
│   │   QNTopologyModel (control the updating of the request pool)
└───Topology (topology generation)
│   │   RouteGenerator (generate the route information by using K_shortest_paths.py)
│   │   k_shortest_paths (generate the top-k candidate routes for the requests)
|   |   TopologyGenerator (generate quantum network topology by using NetworkX and Waxman)
│   │   topology.csv (topology information)
└───Transmitting (transmitting stage)
│   │   BranchBound (brand-and-bounch algorithm example)
│   │   ILP (the improved brand-and-bounch algorithm and LP solver)
│   │   RouteSelection.lp (the optimization model of Gurobi)
│   │   utils (tools)
└───save_graph (transmitting stage)
│   └───agent_training_results_ims (the figures of the training process)
│   │   │   Adjust_fidelity_threshold.pdf (the figure of adjusting fidelity thresholds)
│   │   │   Adjust_delay_threshold.pdf (the figure of adjusting delay thresholds)
│   │   │   Heterogeneous_requests_mu.pdf (the figure of adjusting expectations of the request data volume)
│   │   │   Heterogeneous_requests_sigma.pdf (the figure of adjusting variances of the request data volume)
│   │   │   Node*.pdf (the training convergence of the distributed agents on these nodes )
│   │   │   Node_importance (the node importance generated by ......)
│   │   │   Optimal_comparison_*.pdf (the comparison results with the Sophon_route_optimal)
│   │   │   Sophon_train_*.pdf (the train results of Sophon)
│   │   │   draw* (draw these figures)
└───save_model (save the trained model after the training process)
└───main.py (for running a train process of Sophon)
└───README.md (you are here)
└───requirements.txt (all the necessary packages for running the code)



