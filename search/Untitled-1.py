
    

   
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
