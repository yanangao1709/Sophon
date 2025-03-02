# %%
n = 3

# %%
# 先要求没一行只能出现1个1， 后面转置一下。
def get_all_lines(n):
    res = []
    for i in range(n):
        line = [0] * n
        line[i] = 1
        res.append(line)
    return res
def get_all_matrixs(n):
    res = []
    for i in range(n):
        t_lines = get_all_lines(n) # 当前行所有可能
        # 取出已有所有的行
        if len(res) < 1:
            for line in t_lines:
                res.append([line,]) # 初始化1行
        else:
            t_res = res.copy() # 先复制一下
            res = [] # 清空一下，准备下一次循环
            for m in t_res: # 遍历之前的所有结果(矩阵)
                for line in t_lines:
                    t_m = m.copy() # 复制一下，防止修改
                    t_m.append(line)
                    res.append(t_m)
    return res


def m_transpose(mat): # 矩阵转置
    n = len(mat)
    res = []
    for i in range(n):
        t_line = []
        for j in range(n):
            t_line.append(mat[j][i])
        res.append(t_line)
    return res
        
## 计算概率表示，0-1，或者1-0，概率都为p, 保持不变，则为1
def cal_p(mat):
    n = len(mat)
    # 每一列只能有1个1，找到那个1，计算其概率即可。
    res = []
    all_i_set = set()
    for j in range(n): # 遍历每一列
        flag_i_1 = j  ## 原始矩阵的第j列，第j为位置为1
        for i in range(n): # 遍历每一行, 找到那个1
            if mat[i][j] == 1:
                flag_i_1 = i
                all_i_set.add(i)
        if flag_i_1 == j:
            res.append("(1-p)")
        else:
            res.append(f"(p/{n-1})")
    # 第二个参数表示，是否每一行都出现了1
    return "*".join(res), len(all_i_set) == n

global_all_p = []
line_1_p = []
def m_print(mat, flag = False):
    n = len(mat)
    # 每一行都可以在任意位置出现1，所以的是递归
    p_str, flag_1 = cal_p(mat)
    if flag:
        global_all_p.append(p_str)
    if flag and flag_1:
        line_1_p.append(p_str)
    print(f"=========>: {p_str}")
    for i in range(n):
        print(mat[i])

base_m = [] # 初始化一个初始状态矩阵
for i in range(n):
    line = [0] * n
    line[i] = 1
    base_m.append(line)
print("初始状态矩阵：")
m_print(base_m) # 打印初始状态矩阵

print("所有可能的矩阵：")
res = get_all_matrixs(n)
print(len(res))
for m in res:
    m = m_transpose(m)
    m_print(m, True)
    
# 所有概率求和表示
print("所有概率的和表示：")
print(len(global_all_p))
all_p = "+".join(global_all_p)
print(f"求和: {all_p}")
print()

# 所有每一行有1个1的概率
print("所有每一行有1个1的概率求和：")
line_1_p_str = "+".join(line_1_p)
print(f"求和: {line_1_p_str}")
print()

# %%
# pip install sympy --index-url https://pip.baidu-int.com/simple/

# %%
from sympy import symbols, expand, sympify

# 定义符号
p = symbols('p')

# 定义各个因子的组合
expr = sympify(all_p)
# 展开表达式并简化
expanded_expr = expand(expr)

# 输出展开后的结果
print("Expanded expression:", expanded_expr)


# %%
expr = sympify(line_1_p_str)
# 展开表达式并简化
expanded_expr = expand(expr)

# 输出展开后的结果
print("Expanded expression:", expanded_expr)


# %% [markdown]
# f(2) = 2*p**2 - 2*p + 1
# f(3) = -3*p**3/2 + 15*p**2/4 - 3*p + 1
# f(4) = 40*p**4/27 - 136*p**3/27 + 20*p**2/3 - 4*p + 1
# f(5) = -185*p**5/128 + 1645*p**4/256 - 185*p**3/16 + 85*p**2/8 - 5*p + 1


