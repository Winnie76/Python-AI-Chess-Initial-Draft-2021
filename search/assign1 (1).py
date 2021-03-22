
# match a lower token for each upper token with shortest distance
def func_sort_distance(goal_dictionary):
    sorted_goal_dict = {}
    for key in goal_dictionary:
        min = goal_dictionary[key][0][3]  # minimum distance
        min_i = 0
        for i in range(len(goal_dictionary[key])):
            if goal_dictionary[key][i][3] < min:
                min = goal_dictionary[key][i][3]
                min_i = i
            else:
                pass
        target = {key: goal_dictionary[key][min_i]}
        sorted_goal_dict.update(target)
    return sorted_goal_dict


print(func_sort_distance(goal_dictionary))
token = ('S', -3, 1)


def six_hex_surrond(token):  # find the six surronding hex for a given hex
    if len(token) == 3:
        token = token[1:3]
    action = [[-1, 0], [0, -1], [1, -1], [1, 0], [0, 1],
              [-1, 1]]  # six direction list in clockwise order
    six_hex = []
    for item in action:
        x = item[0]+token[0]
        y = item[1]+token[1]
        loc = (x, y)  # coordinate of the hex
        six_hex.append(loc)
    return six_hex


def if_ol_append(state, item, token, ol):  # check if the item should be added to open list
    if item not in ol:  # to avoid double record
        if item in state:
            # append if not block or undefeatable lower token
            if not ((state[item] == 'Block') | (if_defeat(token, item) == 0)):
                ol.append(item)
        # 这里的else是 如果 item不在state里吗？但如果不在， 那为什么存在？
        else:
            ol.append(item)
    else:
        return ol
    return ol


def open_list(state, token, target):  # record all the possible new location
    # token means upper token
    ol = []
    ol_with_cost = []
    layer1 = six_hex_surrond(token)  # six hex connected to the token

    # slide
    for item in layer1:
        ol = if_ol_append(state, item, token, ol)

    # swing
    for i in range(6):
        item = layer1[i]
        if (item in state):
            if (state[item].isupper()):  # have upper token --> can swing
                # six hex connected to the upper token for swing
                layer2 = six_hex_surrond(item)
                for j in range(i-1, i+2, 1):  # three hex opposite side
                    if (j == 6):  # the hex next to no.5 in the clockwise list is no.0 and no.4
                        ol = if_ol_append(state, layer2[0], token, ol)
                    else:
                        ol = if_ol_append(state, layer2[j], token, ol)
    for item in ol:
        item = list(item)
        cost = func_upper_lower_distance(item, target)
        item.append(cost)
        ol_with_cost.append(item)
    return ol_with_cost


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


# build initial open_close_dict
def open_close_dict_build(state, upper, sorted_goal_dictionary, close_list):
    open_close_dict = {}
    for u in upper:
        u = tuple(u)
        target = sorted_goal_dictionary[u][0]
        ol = open_list(state, token, target)
        mid = {u: [ol, close_list[u]]}
        open_close_dict.update(mid)
    return open_close_dict

# layer1[i]是item
# layer记录顺序按顺时针
# 要记是在layer1 可以用来swing的u2是顺时针记录的list的第几个 (判断在u1的哪个位置）
