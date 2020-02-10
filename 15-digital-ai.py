"""
人工智能大作业1
使用A*算法解决15数码的问题，编写解决函数，并实现题目中的例子：
11 9 4  15       1  2  3  4
1  3 0  12  -->  5  6  7  8
7  5 8  6        9  10 11 12
13 2 10 14       13 14 15 0
找到最优结果，打印输出每一步的运算过程。
"""

import copy


# 定位元素element在state状态中的位置
def locate_element(state, element):
    assert 0 <= element <= 15
    x, y = "", ""
    for i in range(len(state)):
        try:
            x = state[i].index(element)
            y = i
        except ValueError:
            pass
    assert isinstance(x, int) and isinstance(y, int)
    return y, x


# 将0与上下左右的元素交换，不满足交换条件则返回原状态
# 输入交换前的状态，输出交换后的状态  [0, 3]
# direction:"up","down","left","right"
def swap(state, direction):
    new_state = copy.deepcopy(state)  # 深拷贝一份
    zero_y, zero_x = locate_element(new_state, 0)
    if direction == "up":
        if zero_y >= 1:
            new_state[zero_y][zero_x] = new_state[zero_y-1][zero_x]
            new_state[zero_y-1][zero_x] = 0
        return new_state
    elif direction == "down":
        if zero_y <= 2:
            new_state[zero_y][zero_x] = new_state[zero_y+1][zero_x]
            new_state[zero_y+1][zero_x] = 0
        return new_state
    elif direction == "left":
        if zero_x >= 1:
            new_state[zero_y][zero_x] = new_state[zero_y][zero_x-1]
            new_state[zero_y][zero_x-1] = 0
        return new_state
    elif direction == "right":
        if zero_x <= 2:
            new_state[zero_y][zero_x] = new_state[zero_y][zero_x+1]
            new_state[zero_y][zero_x+1] = 0
        return new_state
    else:
        raise("input error in function swap !")


# 计算估价函数f(n)=g(n)+h(n), g(n) = tree_deep
def evaluation_function(state, tree_deep, final_state):
    h_n = 0
    for i in range(0,16,1):
        y1, x1 = locate_element(state, i)
        y2, x2 = locate_element(final_state, i)
        h_n += abs(y1-y2) + abs(x1-x2)
    return h_n + tree_deep


# 在closed表中寻找最优解路径，返回想查找[state,num,father_num]的所有父节点列表,直到father_num=0
def search_optimal_path(closed_list, state_pack):
    if closed_list == []:
        return []
    res_path = [state_pack]
    fa = state_pack[2]
    while fa != 0:
        res_path.append(closed_list[fa])
        fa = closed_list[fa][2]
    return res_path


# 使用A*算法进行启发式搜索的主函数
# 输入的state_initial size 4x4, state_target size 4x4
def solve(state_initial, state_target):
    open_list = []
    closed_list = []
    history_list = []
    evaluation_open_list = []
    open_list.append([state_initial, 0, 0])  # 后两个参数为第几层，父节点是哪号
    evaluation_open_list.append(evaluation_function(state_initial, 0, state_target))
    history_list.append(state_initial)
    while open_list != []:  # open_list 不为空时
        min_evaluation_index = evaluation_open_list.index(min(evaluation_open_list))
        # 扩展这个节点
        state = open_list.pop(min_evaluation_index)
        evaluation_open_list.pop(min_evaluation_index)
        print(state)
        # 判断open_list第一个元素是不是target
        if state[0] == state_target:
            print(search_optimal_path(closed_list, state))
            break
        closed_list.append(state)
        for direction in ["up", "down", "left", "right"]:
            new_state = swap(state[0], direction)
            if new_state not in history_list:
                tree_deep = closed_list[-1][1]+1
                open_list.append([new_state, tree_deep, len(closed_list)-1])
                evaluation_open_list.append(evaluation_function(new_state, tree_deep, state_target))
                history_list.append(new_state)


if __name__ == "__main__":
    state_initial = [[11,9,4,15],[1,3,0,12],[7,5,8,6],[13,2,10,14]]
    state_target = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    import timeit
    t1 = timeit.default_timer()
    solve(state_initial, state_target)  # 目标和结果一致时需考虑
    t2 = timeit.default_timer()
    print("run time:", t2-t1)
