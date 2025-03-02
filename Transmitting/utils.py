# 即用工具

class LP_solution:
    def __init__(self, solution, r, route):
        self.solution = solution
        self.r = r
        self.route = route

def is_sublist(sublist, mainlist):
    if sublist == None:
        return True
    n = len(sublist)
    for i in range(len(mainlist) - n + 1):
        if mainlist[i:i+n] == sublist:
            return True
    return False

def find_overlap_node(route1, route2):
    r_len = min(len(route1), len(route2))
    flag = False
    for point in range(r_len):
        if route1[point] == route2[point]:
            return point
        else:
            break
    if not flag:
        return -1