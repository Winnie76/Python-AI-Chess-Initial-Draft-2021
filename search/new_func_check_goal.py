def func_check_goal_reached(upper_tuple, sorted_goal_dict, open_close_dict):
    if upper_tuple in sorted_goal_dict.keys():
        # if last element in close list is the same as sorted goal dict first goal
        #position is an index list
        position=[]
        for i in range(len(sorted_goal_dict[upper_tuple])):
            if open_close_dict[upper_tuple][1][-1] == sorted_goal_dict[upper_tuple][i][1:3]:
                position.append(i)
            #print('open_close_dict[upper_tuple][1][-1]:', open_close_dict[upper_tuple][1][-1])
            #print('sorted_goal_dict[upper_tuple][0][1:3]', sorted_goal_dict[upper_tuple][0][1:3])
            # if the length of goals of sorted goal dict is 1 --> remove that key value pair from sorted_goal_dict
        if (position): #defeat the current goal
            if len(sorted_goal_dict[upper_tuple]) == 1:
                del sorted_goal_dict[upper_tuple]
            # if more than 1 goal in sorted_goal_dict
            else:
                #delete the goal in dict by finding the index
                del sorted_goal_dict[upper_tuple][position[0]]
    open_close_dict[upper_tuple][0] = []

    return open_close_dict
