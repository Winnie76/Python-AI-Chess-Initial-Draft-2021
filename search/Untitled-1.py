
    

   
      # loop through all upper tokens again and print next move for all upper tokens
      # why use 2 loops seperately : if one upper token move directly, it's may not be the best move for all upper tokens cuz another upper token needs to change route??
      # maybe can find a way to put into one loop. but i will go with this method first
      for upper_tuple in all_uppers_list:
          # upper token already reached all goals
          if upper_tuple not in sorted_goal_dict.keys():
              # NEED func_update_state HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              # func_update_state updates the state 
              # it can check if current upper token reached goal or not
              # if reached goal already, then it will make a best random movement for upper token , update state and print the movement
              # if not reached goal, then based on open_close_list movement, it will update the state according to that and print the movement
              # so the function reads which upper token it is from argument, read the current state, read the open_close_dict to know which movement to update and then update the state
              state = func_update_state(upper_tuple, state, open_close_dict)
        # upper token still have goal to reach
        else:
            # NEED func_update_close HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # func_update_close only updates the close list (which is the action/movement of that upper token) in open_close_dict
            # it read upper_tuple from argument to know which upper token to update
            # it reads open-close_list and make a decision based on all possible moves and current state of board
            open_close_dict = func_update_close( upper_tuple, open_close_list, state)
            # based on open_close_list movement, it will update the state according to that and print the movement
            state = func_update_state(upper_tuple, state, open_close_dict)

            # NEED func_check_goal_reached HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # check if upper token reached goal or not
            # if upper token reached its goal, delete that value in sorted_goal_dict, and delete that upper token (key&value) in open_close_list
            # if upper token reached all goals, delete that key-value pair in sorted_goal_dict, and delete that upper token (key&value) in open_close_list
            if func_check_goal_reached(upper_tuple, sorted_goal_dict, open_close_dict) == 1:
                open_close_dict.remove(upper_tuple)
                # NEED func_remove_value_or_both HERE ~~~~~~~~~~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                sorted_goal_dict = func_remove_value_or_both(upper_tuple, sorted_goal_dict, open_close_dict)



      # max_cost = 0
      # final_random_move = []
      # # possible random move is for current upper token
      # for next_move in possible_random_move:
      #     if next_move not in possible_move_all_tokens:
      #         state[tuple(next_move)] = upper_tuple[0]
      #         print('Turn ', turn, ':', 'GO', ' from ',
      #               upper_tuple[1:3], ' to ', tuple(next_move))
      #         open_close_dict[upper_tuple][1].append(next_move)
      #         del state[tuple(open_close_dict[upper_tuple][1][-2])]
      #         return state
      #     else:
      #         # find next_move in possible move all token and choose the next_move with max cost
      #         cost = possible_with_cost[possible_move_all_tokens.index(
      #             next_move)][2]
      #         # find max cost for random move so that it won't affect other upper tokens'movement
      #         if max_cost < cost:
      #             max_cost = cost
      #             # print('max cost', max_cost)
      #             # final_random_move = [x,y,cost, 'R']
      #             final_random_move = possible_with_cost[possible_move_all_tokens.index(
      #                 next_move)] + [upper_tuple[0]]
      #
      # state[tuple(final_random_move[0:2])] = final_random_move[-1]
      # # print('random')
      # print('Turn ', turn, ':', 'GO', ' from ',
      #       upper_tuple[1:3], ' to ', tuple(final_random_move[0:2]))
      # open_close_dict[upper_tuple][1].append(final_random_move[0:2])
      # # delete the previous position upper token is in the state
      # del state[tuple(open_close_dict[upper_tuple][1][-2])]
      # return state



#print('current open_close_dict', open_close_dict)
        #print('possible random move for this upper token', possible_random_move)
        # all possible moves for all upper tokens at that turn in open lists [[x,y], [x2,y2]......]
        #possible_move_all_tokens = []
        # all possible moves for all upper token at that turn with cost [[x,y,cost],[x2,y2,cost].....]
        # possible_with_cost = []
        # for key in open_close_dict.keys():
        #     possible_with_cost.append(open_close_dict[key][0])
        # print('possible with cost', possible_with_cost)
        # possible_move_all_tokens = [i[0:2] for i in possible_with_cost]
        # print('possible move for alll tokens', possible_move_all_tokens)
        # # print(possible_move_all_tokens)


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



# {(2, -3): 'P', (3, -3): 'R', (4, -2): 'S', (-4, 4): 'r', (-3, -1): 'p', (-3, 1): 'p', (-3, 3): 's', (-2, 4): 'r',
        # (0, 3): 'p', (2, 2): 's', (-1, 1): 'Block', (0, 0): 'Block', (2, -1): 'Block', (2, 0): 'Block', (3, 0): 'Block',
        # (0, -5): 'Block', (1, -5): 'Block', (2, -5): 'Block', (3, -5): 'Block', (4, -5): 'Block', (5, -5): 'Block',
        # (5, -4): 'Block', (5, -3): 'Block', (5, -2): 'Block', (5, -1): 'Block', (5, 0): 'Block', (4, 1): 'Block',
        # (3, 2): 'Block', (2, 3): 'Block', (1, 4): 'Block', (0, 5): 'Block', (-1, 5): 'Block', (-2, 5): 'Block',
        # (-3, 5): 'Block', (-4, 5): 'Block', (-5, 5): 'Block', (-5, 4): 'Block', (-5, 3): 'Block', (-5, 2): 'Block',
        # (-5, 1): 'Block', (-5, 0): 'Block', (-4, -1): 'Block', (-3, -2): 'Block', (-2, -3): 'Block', (-1, -4): 'Block'}


      # print_board(state) -- still this board with no blocks around it
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


      # try print the board using helper function

      # TODO:
      # Find and print a solution to the board configuration described
      # by `data`.
      # Why not start by trying to print this configuration out using the
      # `print_board` helper function? (See the `util.py` source code for
      # usage information).

#此时的state不是最新的，无法通过state找到open list？？？
                    #知道有冲突的upper token叫 upper

      # 这里需要检查其它upper token -1 是不是和min_cost_move 一样才行！！！！！没有写


      # a problem may arise if there is only one possible random move but it is also other token's next move
      # need to change the next move of that token!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
