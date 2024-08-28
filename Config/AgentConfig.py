#
# 强化学习智能体参数设置，实验结果可调参数过程
#
from Config import QNConfig, TopologyConfig

memory_size = 1000
discount_factor = 0.9
learning_rate = 0.001

# 探索参数的自适应调整
epsilon = 0.8
epsilon_min = 0.01
explore_step = 3000
epsilon_decay = (epsilon - epsilon_min) / explore_step

batch_size = 32
step_limit = 10
episodes_length = 10000

X_thr = 4

obs_size = QNConfig.request_pool_len * QNConfig.candidate_route_num + QNConfig.request_pool_len + 1 + TopologyConfig.node_num
# obs_size = QNConfig.request_pool_len + 1
act_size = X_thr