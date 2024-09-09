# 论文中问题定义给出例子的实现
import networkx as nx

nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
G_exp = nx.Graph()
G_exp.add_edge('A', 'B', length=5)
G_exp.add_edge('A', 'D', length=2)
G_exp.add_edge('B', 'C', length=4)
G_exp.add_edge('B', 'D', length=3)
G_exp.add_edge('B', 'E', length=2)
G_exp.add_edge('C', 'E', length=2)
G_exp.add_edge('D', 'E', length=4)
G_exp.add_edge('D', 'F', length=3)
G_exp.add_edge('F', 'G', length=4)
G_exp.add_edge('G', 'H', length=4)
G_exp.add_edge('E', 'H', length=2)
# node_capacity = {'A':4, 'B':5, 'C':4, 'D':6, 'E':3, 'F':4, 'G':4, 'H':2}
node_capacity = {'A':2, 'B':3, 'C':2, 'D':3, 'E':2, 'F':3, 'G':2, 'H':2}
# 绘制并显示拓扑
# nx.draw(G_exp, pos=nx.spring_layout(G_exp), with_labels=True, node_color='y')
# plt.show()

allocated_qubits = 2
candidate_route_num = 2

