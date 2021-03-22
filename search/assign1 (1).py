
def update_open_close(key, open_close_dict, sorted_goal_dict):

    # renew open list, and put movement into close dict
    target = sorted_goal_dict[key][0]
    ol = open_list(state, key, target)
    cl = open_close_dict[key][1]
    min_dis = ol[0][2]
    min_i = 0
    for i in range(len(ol)):  # find the movement with least distance to target
        if ol[i][2] < min_dis:
            min_dis = ol[i][2]
            min_i = i
    cl.append(ol[min_i][0:2])  # renew close list
    # state=func_update_state(state) #renew state
    ol = open_list(state, key, target)  # renew open list
    open_close_dict[key] = [ol, cl]  # renew open_close_list
    return open_close_dict


# layer1[i]是item
# layer记录顺序按顺时针
# 要记是在layer1 可以用来swing的u2是顺时针记录的list的第几个 (判断在u1的哪个位置）
