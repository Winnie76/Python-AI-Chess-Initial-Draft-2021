        if len(all_uppers_list)>1:
            for i in range(1,len(all_uppers_list),1): #insertion sort
                val=len(open_close_dict[all_uppers_list[i]][0])
                val_upper=all_uppers_list[i]
                j=i
                while(len(open_close_dict[all_uppers_list[j-1]][0]) > val):
                    if j<1:
                        break
                    all_uppers_list[j]=all_uppers_list[j-1]
                    j-=1
                all_uppers_list[j]= val_upper
