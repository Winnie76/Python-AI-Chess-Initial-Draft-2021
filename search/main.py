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
        # print(pair[1]) ['p', -1, 3]['s', 1, 3]['r', -2, 4]
        distance = func_upper_lower_distance(pair[0], pair[1])
        # print(distance)--worked
        # print(list(goal_dictionary.keys()))
        if tuple(pair[0]) not in list(goal_dictionary.keys()):
            goal_dictionary[tuple(pair[0])] = [pair[1]+[distance]]
            # print(goal_dictionary[tuple(pair[0])])
        else:
            if pair[1]+[distance] not in goal_dictionary[tuple(pair[0])]:
                goal_dictionary[tuple(pair[0])].append(pair[1]+[distance])
    # print(goal_dictionary)
    # {('P', 2, -3): [['r', -4, 4, 9.219544457292887], ['r', -2, 4, 8.06225774829855]], ('R', 3, -3): [['s', -3, 3, 8.48528137423857], ['s', 2, 2, 5.0990195135927845]], ('S', 4, -2): [['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909], ['p', 0, 3, 6.4031242374328485]]}

    # sorted_goal_dict = sorted dictionary based on distance btw upper and lower token
    sorted_goal_dict = func_sort_distance(goal_dictionary)
    # print(sorted_goal_dict)
    # {('P', 2, -3): [['r', -2, 4, 8.06225774829855], ['r', -4, 4, 9.219544457292887]], ('R', 3, -3): [['s', 2, 2, 5.0990195135927845], ['s', -3, 3, 8.48528137423857]], ('S', 4, -2): [['p', 0, 3, 6.4031242374328485], ['p', -3, -1, 7.0710678118654755], ['p', -3, 1, 7.615773105863909]]}

    # open_close_dict = {(upper token 1): [[open list], [close list]],
    #                   (upper token 2): [[open list], [close list]],
    #                   (upper token 3): [[open list], [close list]],}
    open_close_dict = {}
    # all_uppers_list = [('P', 2, -3), ('R', 3, -3), ('S', 4, -2)]pl
    all_uppers_list = list(goal_dictionary.keys())

    # turn = 0
    # while (bool(sorted_goal_dict) == True) and (turn == 0):
    #     turn += 1
    #     # loop through all upper tokens and put possible moves into open list of open_close_dict
    #     for upper_tuple in all_uppers_list:
    #         if upper_tuple in sorted_goal_dict.keys():
    #             # print(turn, 'yes')
    #             # NEED func_update_open HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #             # func_update_open put all available next move AND total cost (= prev cost + future cost) for current upper token into the open list (open list is in open_close_dict)
    #             # func_update_open doesn't move upper token, it reads the current upper token tuple from argument;
    #             #                                          reads the corresponding goal from sorted_goal_dict,
    #             #                                          reads the current coordinate upper token is on from close list in open_close_dict
    #             #                                          and put possible moves into open list in open_close_dict by using state_dictionary
    #             open_close_dict = func_update_open(
    #                 upper_tuple, open_close_dict, sorted_goal_dict, state)


#--------------------------------------------functions needed-------------------------------------------------------#
# def func_update_open(upper_tuple, open_close_dict, sorted_goal_dict, state):
#     hex_neighbors_list = six_hex_surrond(list(upper_tuple))


# return list of locations [(1,2), (2,5), (-1,3), (0,6), (9,3), (3,4)]
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
