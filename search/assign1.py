

def if_ol_append(state, item, token, ol):  # check if the item should be added to open list
    if item not in ol:  # avoid double record
        if item in state:
            # append if not block or undefeatable lower token
            if not ((state[item] == 'Block') | (if_defeat(token, item) == 0)):
                ol.append(item)
        else:
            ol.append(item)
    else:
        return ol
    return ol


def open_list(state, token):  # record all the possible new location
    # token means upper token
    ol = []
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
    return ol

# layer1[i]是item
# layer记录顺序按顺时针
# 要记是在layer1 可以用来swing的u2是顺时针记录的list的第几个 (判断在u1的哪个位置）
