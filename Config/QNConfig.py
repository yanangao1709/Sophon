# quantum network 参数调整

from Config.TopologyConfig import *


# 分布式智能体，即网络节点数量
agent_num = node_num

# 请求池长度
request_pool_len = 5

# 请求的SD对的候选路径数量，候选路径相关信息存储于QNModel中，由Topology.py产生
candidate_route_num = 3

# 网络节点分布式的局部成本：存储成本系数+register生成成本系数
delta_stor = 1
delta_gen = 1

# 计算路径fidelity参数，纠缠状态产生<1|的概率
p = 0.5

# 退相干散射常数
gamma = 0.1

# 传输阶段，各约束阈值
# fidelity 约束
F_thr = 0.00000001
# delay 约束
D_thr = 150

# 生成请求，所需传输资源的上下限
volume_upper = 20
volume_lower = 10


