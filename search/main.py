"""
COMP30024 Artificial Intelligence, Semester 1, 2021
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""

import sys
import json
import math

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_slide, print_swing


def main():
    try:

        # get the second argument user entered when calling this
        # sys.argv[1]
        with open(sys.argv[1]) as file:
            # so now u have a JSON format data
            data = json.load(file)

        # initiate the current board state
        # change all upper token symbol to UPPER CASE
        for value in data['upper']:
            value[0] = value[0].upper()
        # change all block from '' to 'Block'
        for value in data['block']:
            value[0] = value[0]+'Block'
        upper = data['upper']
        lower = data['lower']
        block = data['block']
        board_limit = board_range()
        for value in board_limit:
            data['block'].append(value)
        state = {}
        for key in data:
            for item in data[key]:
                loc = {tuple(item[1:3]): item[0]}
                state.update(loc)
        # print('state is', state)

    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # find all upper token that can defeat lower token and put into list
    # print(upper) [['S', -1, -1], ['R', 1, -3], ['P', 2, -2]]
    defeatable_list = []
    for upper_token in upper:
        for lower_token in lower:
            if if_defeat(upper_token, lower_token) == 1:
                defeatable_list.append([upper_token, lower_token])

    goal_dictionary = {}
    for pair in defeatable_list:
        distance = func_upper_lower_distance(pair[0], pair[1])
        if tuple(pair[0]) not in list(goal_dictionary.keys()):
            goal_dictionary[tuple(pair[0])] = [pair[1]+[distance]]
        else:
            if pair[1]+[distance] not in goal_dictionary[tuple(pair[0])]:
                goal_dictionary[tuple(pair[0])].append(pair[1]+[distance])
    # print(goal_dictionary)
    # {('P', 2, -3): [['r', -4, 4, 9.219544457292887], ['r', -2, 4, 8.06225774829855]], ('R', 3, -3): [['s', -3, 3, 8.48528137423857], ['s', 2, 2, 5.0990195135927845]], ('S', 4, -2): [['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909], ['p', 0, 3, 6.4031242374328485]]}

    # eliminate repeated goals for different upper tokens
    for upper in goal_dictionary.keys():
        for goal in goal_dictionary[upper]:
            for other_upper in goal_dictionary.keys():
                if upper != other_upper:
                    list_other = [i[0:3] for i in goal_dictionary[other_upper]]

                    if goal[0:3] in list_other:
                        index_other = list_other.index(goal[0:3])
                        remove_goal = goal_dictionary[other_upper][index_other]
                        goal_dictionary[other_upper].remove(remove_goal)
                        break

    sorted_goal_dict = func_sort_distance(goal_dictionary)
    # {('P', 2, -3): [['r', -2, 4, 8.06225774829855], ['r', -4, 4, 9.219544457292887]], ('R', 3, -3): [['s', 2, 2, 5.0990195135927845], ['s', -3, 3, 8.48528137423857]], ('S', 4, -2): [['p', 0, 3, 6.4031242374328485], ['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909]]}

    # open_close_dict = {(upper token 1): [[open list], [close list]],
    #                   (upper token 2): [[open list], [close list]],
    #                   (upper token 3): [[open list], [close list]],}
    open_close_dict = {}
    # print(goal_dictionary) --> {} already empty bc of func_sort_distance
    all_uppers_list = list(sorted_goal_dict.keys())
    # all_uppers_list = [('P', 2, -3), ('R', 3, -3), ('S', 4, -2)]

    # init open_close_dict here
    open_close_dict = open_close_dict_build(
        state, all_uppers_list, sorted_goal_dict)
    #print('build initial open close dict', open_close_dict)
    # print(open_close_dict)
    #  -->  {('P', 2, -3): [[], [[2, -3]]], ('R', 3, -3): [[], [[3, -3]]], ('S', 4, -2): [[], [[4, -2]]]}
    #  {('P', 2, -3): [[[1,2,totol_cost], [2,3,total_cost]......], [[1,2],[2,3],[3,4],.....[target]]], ('R', 3, -3): [[], []], ('S', 4, -2): [[], []]}

    # delete all upper in sorted_goal_dict that has no goals
    new_sorted_goal = {}
    for upper in sorted_goal_dict.keys():
        if sorted_goal_dict[upper] != []:
            new_sorted_goal[upper] = sorted_goal_dict[upper]
    sorted_goal_dict = new_sorted_goal

    turn = 0
    while bool(sorted_goal_dict) == True:

        turn += 1
        # update open list (next possible move) for all upper token
        for upper_tuple in all_uppers_list:
            if upper_tuple in sorted_goal_dict.keys():
                # argument (current state, current upper token position, goal position, list_no_cost=0 )
                open_close_dict[upper_tuple][0] = func_open_list(
                    state, open_close_dict[upper_tuple][1][-1], sorted_goal_dict[upper_tuple][0][0:3], 0)
                # print(open_close_dict)
                # --> {('P', 2, -3): [[[1, -3, 7.615773105863909], [2, -4, 8.94427190999916], [3, -4, 9.433981132056603], [2, -2, 7.211102550927978], [1, -2, 6.708203932499369], [4, -4, 10.0], [4, -3, 9.219544457292887], [3, -2, 7.810249675906654]], [[2, -3]]], ('R', 3, -3): [[[3, -4, 6.082762530298219], [4, -4, 6.324555320336759], [4, -3, 5.385164807134504], [3, -2, 4.123105625617661], [2, -2, 4.0], [1, -2, 4.123105625617661], [1, -3, 5.0990195135927845], [2, -4, 6.0]], [[3, -3]]], ('S', 4, -2): [[[3, -2, 5.830951894845301], [4, -3, 7.211102550927978], [5, -3, 7.810249675906654], [5, -2, 7.0710678118654755], [4, -1, 5.656854249492381], [3, -1, 5.0]], [[4, -2]]]}

        # sort upper token based on len of possible moves
        sorted_open_by_len = {}
        for upper in all_uppers_list:
            sorted_open_by_len[upper] = len(open_close_dict[upper][0])

        sorted_open_by_len = {k: v for k, v in sorted(
            sorted_open_by_len.items(), key=lambda item: item[1])}

        # why use 3 loops seperately : if one upper token move directly, it's may not be the best move for all upper tokens cuz another upper token needs to change route??
        # update close list
        for upper_tuple in sorted_open_by_len.keys():
            # upper token already reached all goals
            if upper_tuple in sorted_goal_dict.keys():

                open_close_dict = func_update_close(
                    upper_tuple, open_close_dict, state)
                # based on open_close_dict movement, it will update the state according to that and print the movement

        # update state and print next move for all upper tokens
        for upper_tuple in all_uppers_list:

            state = func_update_state(
                turn, upper_tuple, state, open_close_dict, sorted_goal_dict)

            func_check_goal_reached(
                upper_tuple, sorted_goal_dict, open_close_dict)

#--------------------------------------------functions needed-------------------------------------------------------#
# check if upper token reached goal or not
# if upper token reached its goal, delete that value in sorted_goal_dict, and delete that upper token (key&value) in open_close_dict
# if upper token reached all goals, delete that key-value pair in sorted_goal_dict, and delete that upper token (key&value) in open_close_dict


def func_check_goal_reached(upper_tuple, sorted_goal_dict, open_close_dict):
    if upper_tuple in sorted_goal_dict.keys():
        # if last element in close list is the same as sorted goal dict first goal
        # position is an index list
        position = []
        for i in range(len(sorted_goal_dict[upper_tuple])):
            if open_close_dict[upper_tuple][1][-1] == sorted_goal_dict[upper_tuple][i][1:3]:
                position.append(i)
        # if the length of goals of sorted goal dict is 1 --> remove that key value pair from sorted_goal_dict
        if (position):  # defeat the current goal
            if len(sorted_goal_dict[upper_tuple]) == 1:
                del sorted_goal_dict[upper_tuple]
            # if more than 1 goal in sorted_goal_dict
            else:
                # delete the goal in dict by finding the index
                del sorted_goal_dict[upper_tuple][position[0]]
                # recalculate distance btw upper and its goal in sorted goal dict    [['r', -2, 4, 8.06225774829855], ['r', -4, 4, 9.219544457292887]]
                for upper_goal in sorted_goal_dict[upper_tuple]:
                    #print('distance', open_close_dict[upper_tuple][1][-1],  upper_goal[1:3])
                    new_distance = func_upper_lower_distance(
                        open_close_dict[upper_tuple][1][-1], upper_goal[1:3])
                    upper_goal[3] = new_distance
                sorted_goal_dict[upper_tuple].sort(key=lambda x: x[3])
    open_close_dict[upper_tuple][0] = []

    return open_close_dict


def board_range():
    v1 = [0, -5]
    v2 = [5, -5]
    v3 = [5, 0]
    v4 = [0, 5]
    v5 = [-5, 5]
    v6 = [-5, 0]
    range_limit = []
    r = v1[0]
    q = v1[1]
    for i in range(6):
        r_q = ['Block', r + i, q]
        range_limit.append(r_q)
    r = v2[0]
    q = v2[1]
    for i in range(1, 6, 1):
        r_q = ['Block', r, q + i]
        range_limit.append(r_q)
    r = v3[0]
    q = v3[1]
    for i in range(1, 6, 1):
        r_q = ['Block', r - i, q + i]
        range_limit.append(r_q)
    r = v4[0]
    q = v4[1]
    for i in range(1, 6, 1):
        r_q = ['Block', r - i, q]
        range_limit.append(r_q)
    r = v5[0]
    q = v5[1]
    for i in range(1, 6, 1):
        r_q = ['Block', r, q - i]
        range_limit.append(r_q)
    r = v6[0]
    q = v6[1]
    for i in range(1, 6, 1):
        r_q = ['Block', r + i, q - i]
        range_limit.append(r_q)
    return range_limit


# func_update_close only updates the close list (which is the action/movement of that upper token) in open_close_dict
# it read upper_tuple from argument to know which upper token to update
# it reads open-close_list and make a decision based on all possible moves and current state of board
def func_update_close(upper_tuple, open_close_dict, state):

    min_cost_move = func_min_move(open_close_dict, upper_tuple)
    # delete this min_cost_move in other upper tokens
    for upper_tuple_i in list(open_close_dict.keys()):
        if upper_tuple_i != upper_tuple:

            # haven't removed effectively
            for item in open_close_dict[upper_tuple_i][0]:
                if item[0:2] == min_cost_move[0:2]:
                    open_close_dict[upper_tuple_i][0].remove(item)

    # check if goal is around
    open_close_dict[upper_tuple][1].append(min_cost_move[0:2])
    open_close_dict[upper_tuple][0] = []
    return open_close_dict


# this function returns [x, y, cost]
def func_min_move(open_close_dict, upper_tuple):
    cost_list = [i[2] for i in open_close_dict[upper_tuple][0]]
    min_cost_move = []
    if len(cost_list) != 0:
        min_cost_index = cost_list.index(min(cost_list))
        # min_cost_move = e.g. [1, -3, 7.615773105863909]
        min_cost_move = open_close_dict[upper_tuple][0][min_cost_index]
    # prevent infinite loop: if the min_cost_move already existed in the close list, and the current open list has length
    # more than one, then remove that min_cost_move and find a new min_cost_move
    if min_cost_move[0:2] in open_close_dict[upper_tuple][1][-10:]:
        if open_close_dict[upper_tuple][1].index(min_cost_move[0:2]) != -2 and len(open_close_dict[upper_tuple][0]) > 1:
            open_close_dict[upper_tuple][0].remove(min_cost_move)
            min_cost_move = func_min_move(open_close_dict, upper_tuple)
    return min_cost_move


# func_update_state updates the state of the board
# if reached goal already, then it will make a best random movement for upper token , update state and print the movement
# if not reached goal, then based on open_close_dict movement, it will update the state according to that and print the movement
# so the function reads which upper token it is from argument, read the current state, read the open_close_dict to know which movement to update and then update the state
def func_update_state(turn, upper_tuple, state, open_close_dict, sorted_goal_dict):
    # 注意！！！！！！！！！！！！！！！！！！！！！！！random只有写入update close，才逻辑不出错！！！！！下次把这个移动到update close list的地方！！！
    # if upper_tuple already reached the goal
    possible_random_move = []
    if upper_tuple not in sorted_goal_dict.keys():
        # check surroundings to make a best decision
        # print(possible_random_move) --> [[1, -3], [2, -4], [3, -4], [2, -2], [1, -2], [4, -4], [4, -3], [3, -2]]
        possible_random_move = func_open_list(
            state, list(open_close_dict[upper_tuple][1][-1]), ['r', 1, 1], 1)

        if len(possible_random_move) > 1:
            for upper in open_close_dict.keys():
                if upper != upper_tuple:
                    if open_close_dict[upper][1][-1] in possible_random_move:
                        possible_random_move.remove(
                            open_close_dict[upper][1][-1])

        state[tuple(possible_random_move[0])] = upper_tuple[0]
        if slide_or_swing(open_close_dict[upper_tuple][1][-1], possible_random_move[0]) == 'SWING':
            print_swing(turn, open_close_dict[upper_tuple][1][-1][0], open_close_dict[upper_tuple]
                        [1][-1][1], possible_random_move[0][0], possible_random_move[0][1])
        else:
            print_slide(turn, open_close_dict[upper_tuple][1][-1][0], open_close_dict[upper_tuple][1][-1][1],
                        possible_random_move[0][0], possible_random_move[0][1])
        open_close_dict[upper_tuple][1].append(possible_random_move[0])
        # delete the previous position upper token is in the state
        del state[tuple(open_close_dict[upper_tuple][1][-2])]

        if len(possible_random_move) == 1:
            for upper in open_close_dict.keys():
                if upper != upper_tuple and open_close_dict[upper][1][-1] == possible_random_move[0]:

                    # new_possible_move = [[x,y, cost],[]...]
                    new_possible_move = func_open_list(
                        state, open_close_dict[upper][1][-2], ['r', 1, 1], 0)
                    open_close_dict[upper][0] = new_possible_move
                    min_cost_move = func_min_move(open_close_dict, upper)
                    if min_cost_move[0:2] == open_close_dict[upper_tuple][1][-1]:
                        min_cost_move = func_min_move(open_close_dict, upper)
                    open_close_dict[upper][1][-1] = min_cost_move[0:2]
        return state

    else:
        symbol = upper_tuple[0]
        state[tuple(open_close_dict[upper_tuple][1][-1])] = symbol
        if slide_or_swing(open_close_dict[upper_tuple][1][-2], open_close_dict[upper_tuple][1][-1]) == 'SWING':
            print_swing(turn, open_close_dict[upper_tuple][1][-2][0], open_close_dict[upper_tuple][1][-2][1],
                        open_close_dict[upper_tuple][1][-1][0], open_close_dict[upper_tuple][1][-1][1])
        else:
            print_slide(turn, open_close_dict[upper_tuple][1][-2][0], open_close_dict[upper_tuple][1][-2][1],
                        open_close_dict[upper_tuple][1][-1][0], open_close_dict[upper_tuple][1][-1][1])
        del state[tuple(open_close_dict[upper_tuple][1][-2])]
        return state


# from_list [x, y]   to_list[m, n]
def slide_or_swing(from_list, to_list):
    if to_list in six_hex_surrond(from_list):
        text = 'SLIDE'
    else:
        text = 'SWING'
    return text


def open_close_dict_build(state, upper, sorted_goal_dictionary):
    open_close_dict = {}
    for u in upper:
        ol = []
        cl = []
        cl.append(list(u[1:3]))
        mid = {u: [ol, cl]}
        open_close_dict.update(mid)
    return open_close_dict


# func_open_list put all available next move AND total cost (= future cost) for current upper token into the open list (open list is in open_close_dict)
# func_open_list doesn't move upper token, it reads the current upper token position[x, y] from argument (last element of close list in open_close_dict);
#                                          reads the corresponding target ['r', x, y] from sorted_goal_dict,
#                                          and put possible moves into open list in open_close_dict by using state_dictionary
def func_open_list(state, upper_current_pos, target, list_no_cost):
    # upper_current_pos means upper upper_current_pos
    ol = []
    ol_with_cost = []
    # six hex connected to the upper_current_pos
    layer1 = six_hex_surrond(upper_current_pos)

    # slide for all possible surrounding hexes
    for surround_item in layer1:
        # surround_item is [1,2]   upper_current_pos is [x, y]
        ol = if_ol_append(state, surround_item, upper_current_pos, ol)

    # swing
    for i in range(6):
        surround_item = layer1[i]
        if (tuple(surround_item) in state):
            # have upper upper_current_pos --> can swing
            if (state[tuple(surround_item)].isupper()):
                # six hex connected to the upper upper_current_pos for swing
                layer2 = six_hex_surrond(surround_item)
                for j in range(i-1, i+2, 1):  # three hex opposite side
                    if (j == 6):  # the hex next to no.5 in the clockwise list is no.0 and no.4
                        ol = if_ol_append(
                            state, layer2[0], upper_current_pos, ol)
                    else:
                        ol = if_ol_append(
                            state, layer2[j], upper_current_pos, ol)
    if list_no_cost == 1:
        return ol
    for movable_hex in ol:
        movable_hex = list(movable_hex)
        # print('movable_hex', movable_hex, 'target', target)
        cost = func_upper_lower_distance(movable_hex, target)
        movable_hex.append(cost)
        ol_with_cost.append(movable_hex)

    return ol_with_cost

# surround_item is [1,2]   upper_current_pos is [x, y]
# ol = if_ol_append(state, surround_item, upper_current_pos, ol)

# (state, surround_item, upper_current_pos, ol)


def if_ol_append(state, item, token, ol):  # check if the item should be added to open list

    new_ol = [i[0:2] for i in ol]

    if item not in new_ol:  # to avoid double record
        if tuple(item) in state:
            ut = [state[tuple(token)]]+[token]
            lt = [state[tuple(item)]]+[item]
            # append if not block or undefeatable lower token (upper, lower) uppper couldn't defeat lower --> 0
            if not ((state[tuple(item)] == 'Block') | (if_defeat(ut, lt) == 0)):
                ol.append(item)
        else:
            ol.append(item)
    else:
        return ol
    return ol


# return list of locations [[1,2], [2,5], [-1,]), [0,6], [9,3], [3,4]]
def six_hex_surrond(token):  # find the six surronding hex for a given hex
    if len(token) == 3:
        token = token[1:3]
    action = [[-1, 0], [0, -1], [1, -1], [1, 0], [0, 1],
              [-1, 1]]  # six direction list in clockwise order
    six_hex = []
    for item in action:
        x = item[0]+token[0]
        y = item[1]+token[1]
        loc = [x, y]  # coordinate of the hex
        six_hex.append(loc)
    return six_hex


# {('P', 2, -3): [['r', -2, 4, 8.06225774829855], ['r', -4, 4, 9.219544457292887]], ('R', 3, -3): [['s', 2, 2, 5.0990195135927845], [
# 's', -3, 3, 8.48528137423857]], ('S', 4, -2): [['p', 0, 3, 6.4031242374328485], ['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909]]}
def func_sort_distance(goal_dictionary):
    sorted_goal_dict = {}
    while bool(goal_dictionary) == True:
        for key in list(goal_dictionary.keys()):
            if goal_dictionary[key] == []:
                sorted_goal_dict[key] = []
                del goal_dictionary[key]
            else:
                min = goal_dictionary[key][0][3]  # minimum distance
                min_i = 0
                for i in range(len(goal_dictionary[key])):
                    if goal_dictionary[key][i][3] < min:
                        min = goal_dictionary[key][i][3]
                        min_i = i
                    else:
                        pass
                if key not in list(sorted_goal_dict.keys()):
                    target = {key: [goal_dictionary[key][min_i]]}
                    sorted_goal_dict.update(target)
                else:
                    sorted_goal_dict[key].append(goal_dictionary[key][min_i])

                goal_dictionary[key] = [
                    i for i in goal_dictionary[key] if i[3] != min]
                if goal_dictionary[key] == []:
                    del goal_dictionary[key]
    return sorted_goal_dict


def func_upper_lower_distance(ut, lt):
    if len(ut) == 2 and len(lt) == 2:
        distance = math.sqrt((ut[1] - lt[1]) ** 2 + (ut[0] - lt[0]) ** 2)
        return distance
    if len(ut) == 2:
        distance = math.sqrt((ut[1]-lt[2])**2 + (ut[0]-lt[1])**2)
        return distance
    distance = math.sqrt((ut[2]-lt[2])**2 + (ut[1]-lt[1])**2)
    return distance

# ut lt are tuples ('R', x, y) or ['R', x, y]


def if_defeat(ut, lt):
    if (ut[0] == 'S') & (lt[0] == 'p'):
        return 1
    elif (ut[0] == 'R') & (lt[0] == 's'):
        return 1
    elif (ut[0] == 'P') & (lt[0] == 'r'):
        return 1
    else:
        return 0
