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
        with open('test.json') as file:
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
        state = {}
        for key in data:
            for item in data[key]:
                loc = {tuple(item[1:3]): item[0]}
                state.update(loc)
        # print('state is', state)
        # {(2, -3): 'P', (3, -3): 'R', (4, -2): 'S', (-4, 4): 'r', (-3, -1): 'p', (-3, 1): 'p', (-3, 3): 's', (-2, 4): 'r', (0, 3): 'p', (2, 2): 's', (-1, 1): 'Block', (0, 0): 'Block', (2, -1): 'Block', (2, 0): 'Block', (3, 0): 'Block'}

        # print_board(state)
        #              .-'-._.-'-._.-'-._.-'-._.-'-.
        #             |     |     |  S  |     |     |
        #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #          |     |  R  |     |     |Block|     |
        #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #       |     |  P  |     |Block|Block|     |  s  |
        #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        #    |     |     |     |     |     |     |     |     |
        #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
        # |     |     |     |     |Block|     |     |  p  |     |
        # '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #    |     |     |     |     |Block|     |     |     |
        #    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #       |     |     |     |     |     |     |  r  |
        #       '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #          |  p  |     |  p  |     |  s  |     |
        #          '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #             |     |     |     |     |  r  |
        #             '-._.-'-._.-'-._.-'-._.-'-._.-'

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
    # print(defeatable_list) --working

    goal_dictionary = {}
    for pair in defeatable_list:
        # print(pair[0])['S', -1, -1]['R', 1, -3]['P', 2, -2]
        #      (pair[1]) ['p', -1, 3]['s', 1, 3]['r', -2, 4]
        distance = func_upper_lower_distance(pair[0], pair[1])
        if tuple(pair[0]) not in list(goal_dictionary.keys()):
            goal_dictionary[tuple(pair[0])] = [pair[1]+[distance]]
        else:
            if pair[1]+[distance] not in goal_dictionary[tuple(pair[0])]:
                goal_dictionary[tuple(pair[0])].append(pair[1]+[distance])
    # print(goal_dictionary)
    # {('P', 2, -3): [['r', -4, 4, 9.219544457292887], ['r', -2, 4, 8.06225774829855]], ('R', 3, -3): [['s', -3, 3, 8.48528137423857], ['s', 2, 2, 5.0990195135927845]], ('S', 4, -2): [['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909], ['p', 0, 3, 6.4031242374328485]]}
    sorted_goal_dict = func_sort_distance(goal_dictionary)
    # print(sorted_goal_dict)
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
    # print(open_close_dict)
    #  -->  {('P', 2, -3): [[], [[2, -3]]], ('R', 3, -3): [[], [[3, -3]]], ('S', 4, -2): [[], [[4, -2]]]}
    # i want {('P', 2, -3): [[[1,2,totol_cost], [2,3,total_cost]......], [[1,2],[2,3],[3,4],.....[target]]], ('R', 3, -3): [[], []], ('S', 4, -2): [[], []]}

    # del sorted_goal_dict[('P', 2, -3)]
    turn = 0
    # while (bool(sorted_goal_dict) == True) and (turn == 0):
    while bool(sorted_goal_dict) == True:
        turn += 1
        # update open list (next possible move) for all upper token
        for upper_tuple in all_uppers_list:
            if upper_tuple in sorted_goal_dict.keys():
                # update open list
                open_close_dict[upper_tuple][0] = func_open_list(
                    state, open_close_dict[upper_tuple][1][-1], sorted_goal_dict[upper_tuple][0][0:3], 0)
                # print(open_close_dict)
                # --> {('P', 2, -3): [[[1, -3, 7.615773105863909], [2, -4, 8.94427190999916], [3, -4, 9.433981132056603], [2, -2, 7.211102550927978], [1, -2, 6.708203932499369], [4, -4, 10.0], [4, -3, 9.219544457292887], [3, -2, 7.810249675906654]], [[2, -3]]], ('R', 3, -3): [[[3, -4, 6.082762530298219], [4, -4, 6.324555320336759], [4, -3, 5.385164807134504], [3, -2, 4.123105625617661], [2, -2, 4.0], [1, -2, 4.123105625617661], [1, -3, 5.0990195135927845], [2, -4, 6.0]], [[3, -3]]], ('S', 4, -2): [[[3, -2, 5.830951894845301], [4, -3, 7.211102550927978], [5, -3, 7.810249675906654], [5, -2, 7.0710678118654755], [4, -1, 5.656854249492381], [3, -1, 5.0]], [[4, -2]]]}

        # loop through all upper tokens again and print next move for all upper tokens
        # why use 2 loops seperately : if one upper token move directly, it's may not be the best move for all upper tokens cuz another upper token needs to change route??
        # maybe can find a way to put into one loop. but i will go with this method first
        # del sorted_goal_dict[('P', 2, -3)]
        for upper_tuple in all_uppers_list:
            # upper token already reached all goals
            if upper_tuple not in sorted_goal_dict.keys():
                # NEED func_update_state HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # func_update_state updates the state
                # if reached goal already, then it will make a best random movement for upper token , update state and print the movement
                # if not reached goal, then based on open_close_dict movement, it will update the state according to that and print the movement
                # so the function reads which upper token it is from argument, read the current state, read the open_close_dict to know which movement to update and then update the state
                state = func_update_state(turn,
                                          upper_tuple, state, open_close_dict, sorted_goal_dict)

            # upper token still have goal to reach
            else:
                open_close_dict = func_update_close(
                    upper_tuple, open_close_dict, state)
                # based on open_close_dict movement, it will update the state according to that and print the movement
                state = func_update_state(
                    turn, upper_tuple, state, open_close_dict, sorted_goal_dict)

                func_check_goal_reached(
                    upper_tuple, sorted_goal_dict, open_close_dict)

#--------------------------------------------functions needed-------------------------------------------------------#
# check if upper token reached goal or not
# if upper token reached its goal, delete that value in sorted_goal_dict, and delete that upper token (key&value) in open_close_dict
# if upper token reached all goals, delete that key-value pair in sorted_goal_dict, and delete that upper token (key&value) in open_close_dict


def func_check_goal_reached(upper_tuple, sorted_goal_dict, open_close_dict):
    if open_close_dict[upper_tuple][1][-1] == sorted_goal_dict[upper_tuple][0][1:3]:
        if len(sorted_goal_dict[upper_tuple]) == 1:
            del sorted_goal_dict[upper_tuple]
        else:
            sorted_goal_dict[upper_tuple] = sorted_goal_dict[upper_tuple][1:]
        del open_close_dict[upper_tuple]


# func_update_close only updates the close list (which is the action/movement of that upper token) in open_close_dict
# it read upper_tuple from argument to know which upper token to update
# it reads open-close_list and make a decision based on all possible moves and current state of board
def func_update_close(upper_tuple, open_close_dict, state):

    min_cost_move = func_min_move(open_close_dict, upper_tuple)

    # delete this min_cost_move in other upper tokens
    for upper_tuple_i in list(open_close_dict.keys()):
        if upper_tuple_i != upper_tuple:
            # print('min_cost_moveeeeeeeeeee', min_cost_move)
            # print('open_close_dict[upper_tuple_i][0]',open_close_dict[upper_tuple_i][0])
            # haven't removed effectively
            if (min_cost_move in open_close_dict[upper_tuple_i][0]) or (min_cost_move[0:2] in open_close_dict[upper_tuple_i][1]):
                # print('yes innnnnn')
                if (min_cost_move in open_close_dict[upper_tuple_i][0]):
                    open_close_dict[upper_tuple_i][0].remove(min_cost_move)
                else:
                    open_close_dict[upper_tuple][0].remove(min_cost_move)
                    min_cost_move = func_min_move(
                        open_close_dict, upper_tuple)
                # print('yes removed', min_cost_move)
    open_close_dict[upper_tuple][1].append(min_cost_move[0:2])
    open_close_dict[upper_tuple][0] = []
    # print('current open_close_dict', open_close_dict)
    return open_close_dict
    # min_move_other_upper = []
    # for upper_tuple_i in list(open_close_dict.keys()):
    #     if upper_tuple_i != upper_tuple:
    #         min_move_other_upper.append(
    #             func_min_move(open_close_dict, upper_tuple_i))

    # same_min_move = 0
    # for other_move in min_move_other_upper:
    #     if other_move == min_cost_move:
    #         same_min_move += 1

    # if same_min_move == 2:
    #     print('ERROR--2 SAME MIN_MOVE--NO ALGO WROTE FOR THIS CASE--NEED TO WRITE ONE ALGO')
    #     open_close_dict[upper_tuple][0].remove(min_cost_move)
    #     min_move = func_min_move(open_close_dict, upper_tuple)
    #     if min_move[0:2] in open_close_dict[upper_tuple][1]:
    #         open_close_dict[upper_tuple][0].remove(min_move)
    #         min_move = func_min_move(open_close_dict, upper_tuple)
    #         # del that element
    #         # cal again min_move
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict
    #     else:
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict
    #     # sys.exit()
    # if same_min_move == 1:
    #     if len(open_close_dict[upper_tuple][0]) > 1:
    #         open_close_dict[upper_tuple][0].remove(min_cost_move)
    #         min_move = func_min_move(open_close_dict, upper_tuple)
    #     else:
    #         # if other token len > 1
    #         # del min move inside other token
    #         # else
    #         # current token
    #     if min_move[0:2] in open_close_dict[upper_tuple][1]:
    #         open_close_dict[upper_tuple][0].remove(min_move)
    #         min_move = func_min_move(open_close_dict, upper_tuple)
    #         # del that element
    #         # cal again min_move
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict
    #     else:
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict
    # else:
    #     min_move = func_min_move(open_close_dict, upper_tuple)
    #     if min_move[0:2] in open_close_dict[upper_tuple][1]:
    #         open_close_dict[upper_tuple][0].remove(min_move)
    #         min_move = func_min_move(open_close_dict, upper_tuple)
    #         # del that element
    #         # cal again min_move
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict
    #     else:
    #         open_close_dict[upper_tuple][1].append(list(min_move[0:2]))
    #         open_close_dict[upper_tuple][0] = []
    #         return open_close_dict


# return [x, y, cost]
def func_min_move(open_close_dict, upper_tuple):
    cost_list = [i[2] for i in open_close_dict[upper_tuple][0]]
    min_cost_move = []
    if len(cost_list) != 0:
        min_cost_index = cost_list.index(min(cost_list))
        # min_cost_move = e.g. [1, -3, 7.615773105863909]
        min_cost_move = open_close_dict[upper_tuple][0][min_cost_index]
    # prevent infinite loop
    if min_cost_move[0:2] in open_close_dict[upper_tuple][1]:
        if open_close_dict[upper_tuple][1].index(min_cost_move[0:2]) != -2:
            open_close_dict[upper_tuple][0].remove(min_cost_move)
            min_cost_move = func_min_move(open_close_dict, upper_tuple)
    return min_cost_move

# update the state of board


def func_update_state(turn, upper_tuple, state, open_close_dict, sorted_goal_dict):

    # if upper_tuple already reached the goal
    possible_random_move = []
    if upper_tuple not in sorted_goal_dict.keys():
        # check surroundings to make a best decision
        # print(possible_random_move) --> [[1, -3], [2, -4], [3, -4], [2, -2], [1, -2], [4, -4], [4, -3], [3, -2]]
        possible_random_move = func_open_list(
            state, list(upper_tuple[1:3]), ['r', 1, 1], 1)

        # all possible moves for all upper tokens at that turn in open lists [[x,y], [x2,y2]......]
        possible_move_all_tokens = []
        # all possible moves for all upper token at that turn with cost [[x,y,cost],[x2,y2,cost].....]
        possible_with_cost = []
        for key in open_close_dict:
            possible_with_cost += open_close_dict[key][0]
        possible_move_all_tokens = [i[0:2] for i in possible_with_cost]
        # print(possible_move_all_tokens)

        max_cost = 0
        final_random_move = []
        for next_move in possible_random_move:
            if next_move not in possible_move_all_tokens:
                state[tuple(next_move)] = upper_tuple[0]
                print('Turn ', turn, ':', 'GO', ' from ',
                      upper_tuple[1:3], ' to ', tuple(next_move))
                del state[upper_tuple[1:3]]
                return state
            else:
                cost = possible_with_cost[possible_move_all_tokens.index(
                    next_move)][2]
                # find max cost for random move so that it won't affect other upper tokens'movement
                if max_cost < cost:
                    max_cost = cost
                    # print('max cost', max_cost)
                    # final_random_move = [x,y,cost]
                    final_random_move = possible_with_cost[possible_move_all_tokens.index(
                        next_move)] + [upper_tuple[0]]

        state[tuple(final_random_move[0:2])] = final_random_move[-1]
        # print('random')
        print('Turn ', turn, ':', 'GO', ' from ',
              upper_tuple[1:3], ' to ', tuple(final_random_move[0:2]))
        del state[upper_tuple[1:3]]
        return state

    else:
        symbol = state[tuple(open_close_dict[upper_tuple][1][-2])]
        # print('symbol is', symbol)
        state[tuple(open_close_dict[upper_tuple][1][-1])] = symbol
        # print('not random')
        print('Turn ', turn, ':', 'GO', ' from ',
              upper_tuple[1:3], ' to ', tuple(open_close_dict[upper_tuple][1][-1]))
        del state[tuple(open_close_dict[upper_tuple][1][-2])]
        return state


def open_close_dict_build(state, upper, sorted_goal_dictionary):
    open_close_dict = {}
    for u in upper:
        # target = sorted_goal_dictionary[u][0]
        # ol = func_open_list(state, list(u), target)
        # cl = close_list[u]
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
        # surround_item is [1,2]
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


def if_ol_append(state, item, token, ol):  # check if the item should be added to open list
    new_ol = []
    for element in ol:
        new_ol.append(element[0:2])
    if item not in new_ol:  # to avoid double record
        if tuple(item) in state:
            # append if not block or undefeatable lower token
            if not ((state[tuple(item)] == 'Block') | (if_defeat(token, item) == 0)):
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
    if len(ut) == 2:
        distance = math.sqrt((ut[1]-lt[2])**2 + (ut[0]-lt[1])**2)
        return distance
    distance = math.sqrt((ut[2]-lt[2])**2 + (ut[1]-lt[1])**2)
    return distance


def if_defeat(ut, lt):
    if (ut[0] == 'S') & (lt[0] == 'p'):
        return 1
    elif (ut[0] == 'R') & (lt[0] == 's'):
        return 1
    elif (ut[0] == 'P') & (lt[0] == 'r'):
        return 1
    else:
        return 0

    # try print the board using helper function

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).
