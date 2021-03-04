import random
def default_probability(name, home):
    myrange = home[name]['range']
    res = {}.fromkeys(x for x in range(1, myrange))
    for k in res.keys():
        res[k] = 1.0 / (myrange-1)
    return res
#
def current_probability(name, home):
    myrange = home[name]['range']
    res = {}.fromkeys(x for x in range(1, myrange))
    for k in res.keys():
        if (home[name]['frequency'][k]) == None:
            home[name]['frequency'][k] = 0
        val = (home[name]['frequency'][k]) / (home[name]['len'])
        res[k] = val
    return res
#
def group_count(name, home):
    result =   {1 : [0, 0, 0, 0, 0, 0, 0, 0],
                2 : [0, 0, 0, 0, 0, 0, 0, 0],
                3 : [0, 0, 0, 0, 0, 0, 0, 0],
                4 : [0, 0, 0, 0, 0, 0, 0, 0],
                5 : [0, 0, 0, 0, 0, 0, 0, 0],
                6 : [0, 0, 0, 0, 0, 0, 0, 0]}
    
    for lines in home[name]['data']:
        index = 1
        for num in lines:
            result[index][num // 10] += 1
            index +=1
    return result
#
def make_parity(play):
    result = ''
    for num in play:
        if num % 2 == 0:
            result = result + '0'
        else:
            result = result + '1'
    return result
#
def is_in_parity(name, home, play):
    lst = home[name]['parity_simplify'].keys()
    #print(len(lst))
    for par in lst:
        if par == play:
            return True
    return False
#
def won_already(name, home, play):
    for num in home[name]['data']:
        if num == play:
            return True
    return False
# return true if a value is in the list. is_in(list, item)
def is_in(list, item):
    if type(item) == 'list' and len(item) > 1:
        for things in list:
            state = True
            for i in range(len(item)):
                if things[i] == item[i]:
                    continue
                else:
                    state = False
                    break
            if state:
                return True
        return state
    else:
        for things in list:
            if things == item:
                return True
        return False
# This keep track to see how many time a number from the previous two playes show up again in the next play.
def passTwo(name, home):
    data = home[name]['data']
    index = len(data) - 4
    count1 = 0
    count2 = 0
    state = True
    while (index >= 0):
        state = True
        for num in data[index]:
            for i in range(1, 2):
                state = state and  (not is_in(data[index + i], num))
        if state:
            count1 += 1
        else:
            count2 -= 1
        index -= 1
    print('The count 1 is : ', count1, ' and count 2 is : ', count2)
# this counts the number of time a ticket has won.
def count_it(name, Home, play):
    count = 0
    index = 0
    for p in Home[name]['data']:
        index = 0
        state = True
        for n in p:
             state = state and (n == play[index])
             index += 1
        if state:
            count += 1
    return count
#
def ticket_to_string(play):
    result = ''
    for n in play:
        result = result + str(n) + "-"
    return result[:len(result) - 1]
#
def format_(name, play):
    index = 0
    state = True
    if name == 'lotto':
        for num in play:
            if index == 0:
                state = state and (num <= 9)
            elif index == 1:
                state = state and (num >= 1 and num <= 19)
            elif index == 2:
                state = state and (num >= 10 and num <= 29)
            elif index == 3:
                state = state and (num >= 20 and num <= 39)
            elif index == 4:
                state = state and (num >= 20 and num <= 40)
            elif index == 5:
                state = state and (num >= 30 and num <= 44)
            index += 1
    elif name == 'cash5':
        for num in play:
            if index == 0:
                state = state and (num >= 1 and num <= 9)
            elif index == 1:
                state = state and (num >= 1 and num <= 19)
            elif index == 2:
                state = state and (num >= 10 and num <= 29)
            elif index == 3:
                state = state and (num >= 20 and num <= 29)
            elif index == 4:
                state = state and (num >= 20 and num <= 35)
            index += 1
    return state
#
def test(name, Home):
    y = 6
    if name == 'cash5':
        y = 5
    play = []
    for i in range(0, y):
        play.append(int(input(f"Please enter the {i+1} number.")))
    print(play)
    print(f"Is in parity group? : {is_in_parity(name, Home, make_parity(name, play))}")
    print(f"Does it follow winning format:: {format_(name, Home, play)}")
    print('Has it won already? : ', won_already(name, Home, play))
#
def group_plays(name, Home):
    result = {} #this
    for p in Home[name]['data']:
        string = getGroupFormat(p)
        if (is_in(list(result.keys()), string)):
            result[string] += 1
        else:
            result[string] = 1
    return result
#
def test2(name, lst):
    y = 6
    if name == 'cash5':
        y = 5
    play = []
    for i in range(0, y):
        play.append(int(input(f"Please enter the {i+1} number.")))
    print('Is play[{play}] in the filtered set? : ', is_in(lst, play))

# Returns a string that contains the grouping of each number.
def getGroupFormat(p): 
    string = ""
    for x in p:
            string += (str(x // 10))
    return string
# Filter one removes all of the tickets that have won before
def filter_1(name, Home, plays):
    Filter1 = []
    for p in plays:
        if (not (p in Home[name]['data'])):
            Filter1.append(p)
    return Filter1
# Filter two removes all of the grouping that happens less than 60.
def filter_2(Filter1, mygroups, l):
    mykeys = list(mygroups.keys())
    Filter2 = []
    for p in Filter1:
        i = getGroupFormat(p)
        if (i in mykeys) and (mygroups[i] > 60): # migth have to nest these conditions as nested if's.
            Filter2.append(p)
    return Filter2
# Filter three removes all of the plays that don't follow the format.
def filter_3(name, Filter2, l):
    Filter3 = []
    for p in Filter2:
        if format_(name, p):
            Filter3.append(p)
    return Filter3
#
def whole(name, Home, mygroups):
    result = {}
    for k, c in mygroups.items():
        temp = {}
        for p in Home[name]['data']:
            if getGroupFormat(p) == k:
                pp = make_parity(p)
                if pp in list(temp.keys()):
                    temp[pp] += 1
                else:
                    temp[pp] = 1
        result[k] = [c, temp]
    return result
# returns the mode of a string
def mode(lst):
    max = 0
    for a in lst:
        b = lst.count(a)
        if max < b:
            max = b
    return max
# returns the number of character that a and b have in common.
def consecutive_common(a, b):
    result = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            result += 1
        else:
            pass#return result
    return result
#
def in_common(a, b):
    result = 0
    for x in a:
        if x in b:
            result += 1
        else:
            pass#return result
    return result
#
def print_whole(result):
    count = 0
    sum = 0
    for k, c in result.items():
        print(f"Key is : [{k}] : Frequency is : {c[0]}")
        sum = 0
        if count == 32:
            break#sys.exit()
        for k1, v1 in c[1].items():
            print(" "*10, "Key : ", k1, " : ", v1)
            sum += v1
        print("The Sum is : ", sum)
        count += 1
#
def print_is_in(lst, test):
    i = 0
    for p in test:
        if is_in(lst, p):
            i += 1
    return i
# mode filter; REMOVES the groups that repeat more than 3 times.
def mode_filter(lst):
    gf = []
    not_gf = []
    for p in lst:
        if mode(getGroupFormat(p)) < 3:
            gf.append(p)
        else:
            not_gf.append(p)
    return gf, not_gf

def write(lst, name):
    f = open(name, 'w')
    for p in lst:
        f.write((str(p)+"\n"))
    f.close()

def reads(name):
    f = open(name, 'r')
    lst = list(f.read().split('\n'))
    f.close()
    return lst

def getTickets(name):
    result = []
    lst = reads(name)
    n = (int(input(f"How many tickets would you like to play? :....")))
    while n > 0:
        x = random.randint(0, len(lst) - 1)
        while lst[x] in result:
            x = random.randint(0, len(lst) - 1)
        result.append(lst[x])
        n -= 1
    return result

