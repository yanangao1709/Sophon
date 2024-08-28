# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     Author: Yanan Gao                                       #
#       Date: 13-06-2023                                      #
#      Goals: topology data for TOQN                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 量子网络模型1
from Config import QNConfig

# request pool
# Attention!! Networkx表示的拓扑里，节点ID没有0点
REQUESTSET = [[7, 8], [15, 5], [6, 5], [16, 4], [7, 13], [13, 14], [18, 9], [12, 18], [1, 11], [18, 16],
                [15, 18], [11, 18], [1, 11], [10, 18], [9, 17], [3, 7], [16, 12], [4, 10], [15, 18], [7, 14]]
# REQUESTSET = [[7, 8], [15, 5], [6, 5], [16, 4], [7, 13],
#               [13, 14], [18, 9], [12, 18], [1, 11], [18, 16],
#               [15, 18], [11, 18], [1, 11], [10, 18], [9, 17]]
# REQUESTSET = [[7, 8], [15, 5], [6, 5], [16, 4], [7, 13],
#               [13, 14], [18, 9], [12, 18], [1, 11], [18, 16]]
# REQUESTSET = [[7, 8], [15, 5], [6, 5], [16, 4], [7, 13]]


# the volumn of each request
D_VOLUMN = [12, 16, 14, 20, 10, 12, 13, 20, 14, 20, 16, 13, 11, 20, 17, 16, 12, 20, 16, 17]
# D_VOLUMN = [12, 16, 14, 20, 10, 12, 13, 20, 14, 20, 16, 13, 11, 20, 17]
# D_VOLUMN = [12, 16, 14, 20, 10, 12, 13, 20, 14, 20]
# D_VOLUMN = [12, 16, 14, 20, 10]

# candidate_route_num routes of each request
ROUTES = [[[7, 5, 8], [7, 6, 2, 5, 8], [7, 5, 4, 8]], [[15, 6, 7, 5], [15, 2, 5], [15, 6, 2, 5]], [[6, 7, 5], [6, 2, 5], [6, 14, 7, 5]], [[16, 11, 10, 9, 4], [16, 11, 5, 4], [16, 13, 11, 10, 9, 4]], [[7, 11, 13], [7, 14, 13], [7, 6, 14, 13]], [[13, 14], [13, 11, 7, 14], [13, 11, 7, 6, 14]], [[18, 8, 9], [18, 12, 10, 9], [18, 12, 11, 10, 9]], [[12, 18], [12, 10, 9, 8, 18], [12, 16, 17, 18]], [[1, 2, 6, 7, 11], [1, 3, 5, 11], [1, 3, 5, 7, 11]], [[18, 12, 16], [18, 12, 11, 16], [18, 12, 11, 13, 16]], [[15, 6, 7, 11, 12, 18], [15, 14, 7, 11, 12, 18], [15, 14, 13, 11, 12, 18]], [[11, 12, 18], [11, 10, 12, 18], [11, 16, 12, 18]], [[1, 2, 6, 7, 11], [1, 3, 5, 11], [1, 3, 5, 7, 11]], [[10, 12, 18], [10, 11, 12, 18], [10, 9, 8, 18]], [[9, 10, 11, 16, 17], [9, 8, 18, 17], [9, 10, 12, 18, 17]], [[3, 5, 7], [3, 6, 7], [3, 1, 2, 6, 7]], [[16, 12], [16, 11, 12], [16, 13, 11, 12]], [[4, 9, 10], [4, 8, 9, 10], [4, 5, 8, 9, 10]], [[15, 6, 7, 11, 12, 18], [15, 14, 7, 11, 12, 18], [15, 14, 13, 11, 12, 18]], [[7, 14], [7, 6, 14], [7, 6, 15, 14]]]
# ROUTES = [[[7, 5, 8], [7, 6, 2, 5, 8], [7, 5, 4, 8]], [[15, 6, 7, 5], [15, 2, 5], [15, 6, 2, 5]], [[6, 7, 5], [6, 2, 5], [6, 14, 7, 5]], [[16, 11, 10, 9, 4], [16, 11, 5, 4], [16, 13, 11, 10, 9, 4]], [[7, 11, 13], [7, 14, 13], [7, 6, 14, 13]], [[13, 14], [13, 11, 7, 14], [13, 11, 7, 6, 14]], [[18, 8, 9], [18, 12, 10, 9], [18, 12, 11, 10, 9]], [[12, 18], [12, 10, 9, 8, 18], [12, 16, 17, 18]], [[1, 2, 6, 7, 11], [1, 3, 5, 11], [1, 3, 5, 7, 11]], [[18, 12, 16], [18, 12, 11, 16], [18, 12, 11, 13, 16]], [[15, 6, 7, 11, 12, 18], [15, 14, 7, 11, 12, 18], [15, 14, 13, 11, 12, 18]], [[11, 12, 18], [11, 10, 12, 18], [11, 16, 12, 18]], [[1, 2, 6, 7, 11], [1, 3, 5, 11], [1, 3, 5, 7, 11]], [[10, 12, 18], [10, 11, 12, 18], [10, 9, 8, 18]], [[9, 10, 11, 16, 17], [9, 8, 18, 17], [9, 10, 12, 18, 17]]]
# ROUTES = [[[7, 5, 8], [7, 6, 2, 5, 8], [7, 5, 4, 8]], [[15, 6, 7, 5], [15, 2, 5], [15, 6, 2, 5]], [[6, 7, 5], [6, 2, 5], [6, 14, 7, 5]], [[16, 11, 10, 9, 4], [16, 11, 5, 4], [16, 13, 11, 10, 9, 4]], [[7, 11, 13], [7, 14, 13], [7, 6, 14, 13]], [[13, 14], [13, 11, 7, 14], [13, 11, 7, 6, 14]], [[18, 8, 9], [18, 12, 10, 9], [18, 12, 11, 10, 9]], [[12, 18], [12, 10, 9, 8, 18], [12, 16, 17, 18]], [[1, 2, 6, 7, 11], [1, 3, 5, 11], [1, 3, 5, 7, 11]], [[18, 12, 16], [18, 12, 11, 16], [18, 12, 11, 13, 16]]]
# ROUTES = [[[7, 5, 8], [7, 6, 2, 5, 8], [7, 5, 4, 8]],
#           [[15, 6, 7, 5], [15, 2, 5], [15, 6, 2, 5]],
#           [[6, 7, 5], [6, 2, 5], [6, 14, 7, 5]],
#           [[16, 11, 10, 9, 4], [16, 11, 5, 4], [16, 13, 11, 10, 9, 4]],
#           [[7, 11, 13], [7, 14, 13], [7, 6, 14, 13]]]

ROUTES_LEN = [[8, 15, 15], [10, 11, 11], [7, 8, 10], [17, 18, 19], [8, 10, 11], [6, 12, 13], [13, 14, 17], [5, 22, 24], [14, 15, 16], [12, 14, 16], [20, 22, 22], [9, 16, 17], [14, 15, 16], [11, 14, 16], [21, 22, 23], [8, 10, 12], [7, 9, 11], [7, 11, 14], [20, 22, 22], [4, 5, 10]]
# ROUTES_LEN = [[8, 15, 15], [10, 11, 11], [7, 8, 10], [17, 18, 19], [8, 10, 11], [6, 12, 13], [13, 14, 17], [5, 22, 24], [14, 15, 16], [12, 14, 16], [20, 22, 22], [9, 16, 17], [14, 15, 16], [11, 14, 16], [21, 22, 23]]
# ROUTES_LEN = [[8, 15, 15], [10, 11, 11], [7, 8, 10], [17, 18, 19], [8, 10, 11], [6, 12, 13], [13, 14, 17], [5, 22, 24], [14, 15, 16], [12, 14, 16]]
# ROUTES_LEN = [[8, 15, 15], [10, 11, 11], [7, 8, 10], [17, 18, 19], [8, 10, 11]]

# 每个链接的物理长度
LINK_LENS = [
    [0, 4, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0],
    [3, 0, 0, 0, 4, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 5, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 4, 5, 0, 0, 4, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 7, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0],
    [0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 5, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 6, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 11],
    [0, 0, 0, 4, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 5, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 5, 0, 0, 5, 0, 4, 3, 0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 4, 0, 0, 0, 0, 7, 0, 5],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 6, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 6, 0, 4, 0, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 7, 4, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 9],
    [0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 5, 0, 0, 0, 0, 9, 0]
]

# r 请求的 k路径 有没有经过这个点
# 生成
# H_RKN = [[[0] * QNConfig.node_num for i in range(QNConfig.candidate_route_num)] for j in range(len(REQUESTSET))]
# for r in range(len(REQUESTSET)):
#     for k,p in enumerate(ROUTES[r]):
#         for n in range(len(p)):
#             H_RKN[r][k][p[n]-1] = 1
# print(H_RKN)

H_RKN = [[[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]], [[1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1]], [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1]], [[1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1]], [[0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]]]
# H_RKN = [[[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]], [[1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1]], [[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1]], [[1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1]]]
# H_RKN = [[[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1]], [[1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1]]]
# H_RKN = [[[0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]], [[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]], [[0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0]], [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]]]

# r的k候选路径的跳数
ROUTES_HOPS = [[3, 5, 4], [4, 3, 4], [3, 3, 4], [5, 4, 6], [3, 3, 4], [2, 4, 5], [3, 4, 5], [2, 5, 4], [5, 4, 5], [3, 4, 5], [6, 6, 6], [3, 4, 4], [5, 4, 5], [3, 4, 4], [5, 4, 5], [3, 3, 5], [2, 3, 4], [3, 4, 5], [6, 6, 6], [2, 3, 4]]
# ROUTES_HOPS = [[3, 5, 4], [4, 3, 4], [3, 3, 4], [5, 4, 6], [3, 3, 4], [2, 4, 5], [3, 4, 5], [2, 5, 4], [5, 4, 5], [3, 4, 5], [6, 6, 6], [3, 4, 4], [5, 4, 5], [3, 4, 4], [5, 4, 5]]
# ROUTES_HOPS = [[3, 5, 4], [4, 3, 4], [3, 3, 4], [5, 4, 6], [3, 3, 4], [2, 4, 5], [3, 4, 5], [2, 5, 4], [5, 4, 5], [3, 4, 5]]
# ROUTES_HOPS = [[3, 5, 4], [4, 3, 4], [3, 3, 4], [5, 4, 6], [3, 3, 4]]

# node capacity
NODE_CPA = [12, 24, 20, 22, 10, 9, 24, 19, 14, 16, 12, 14, 10, 26, 18, 13, 16, 20]