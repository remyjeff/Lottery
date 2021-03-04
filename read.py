from probability import *
import os, sys
from itertools import combinations
import threading
import concurrent.futures
import time
myplays = {
    'cash5':[[8, 11, 22, 28, 35],
            [3, 8, 15, 23, 27],
            [6, 11, 24, 27, 30],
            [10, 12, 15, 27, 34],
            [2, 11, 14,  27, 28],
            [2, 10, 15, 27, 34],
            [1, 11, 13, 25, 31],
            [2, 12, 14, 24, 30],
            [4, 14, 16, 24, 25],
            [2, 11, 22, 24, 31],
            [4, 14, 23, 29, 33],
            [9, 12, 27, 26, 28],
            [3, 6, 17, 22, 33],
            [5, 7, 13, 23, 26],
            [7, 13, 16, 22, 25],
            [3, 12, 25, 27, 35],
            [2, 16, 24, 33, 35],
            [1, 7, 13, 20, 31],
            [3, 8, 14, 21, 32],
            [1, 10, 13, 22, 26]],
    'lotto':[[2, 18, 21, 23, 31, 40],
           [1, 3, 26, 34, 35, 43],
           [1, 15, 27, 36, 38, 44],
           [2, 7, 22, 29, 35, 38],
           [5, 9, 24, 28, 31, 44],
           [4, 11, 28, 33, 42, 44],
           [4, 6, 21, 29, 33, 37],
           [3, 12, 21, 23, 32, 38],
           [8, 12, 25, 26, 31, 34],
           [2, 7, 11, 25, 34, 38],
           [5, 8, 15, 27, 35, 38],
           [5, 8, 13, 25, 36, 41],
           [3, 11, 15, 23, 31, 35],
           [5, 17, 21, 25, 26, 35],
           [2, 9, 15, 23, 34, 41],
           [7, 15, 22, 33, 37, 40],
           [9, 15, 22, 35, 37, 41],
           [9, 10, 14, 33, 35, 42],
           [7, 10, 13, 20, 30, 37],
           [4, 6, 10, 27, 34, 38],
           [5, 9, 10, 19, 32, 33],
           [1, 7, 20, 27, 34, 41],
           [3, 13, 17, 20, 34, 37]]
}
payout = {
    'lotto': {3:2,
              4:44,
              5:1441,
              6:1000000},
    'cash5': {3:10,
              4:300,
              5:100000},
    'life' : {
              2:3,
              3:20,
              4:200,
              5:390000
            },
    'mega' : {
              3:10,
              4:500,
              5:1000000
            },
    'power' : {
              3:7,
              4:100,
              5:1000000
            }
}
# checks for matches
def match(name, play):
    result = []
    for ticket in myplays[name]:
        count = 0
        for num in play:
            if num in ticket:
                count += 1
        print(f" {ticket} : count is {count} play is {play}")
        result.append(count)
    return result
#
def check_wins():
    result = []
    play = []
    name = input("which play do you want to check:  ")
    num = 0
    c = 1
    while c:
        num = (int)(input(f"Enter number {c}:  "))
        if num == 0:
            result.append({name:match(name, play)})
            play = []
            c = 1
            name = input("What other play do you want to check:  ")
            if name == '0':
                break
        else:
            play.append(num)
            c += 1
    print(result)
    return result

def wins(matches):
    result = 0
    for games in matches:
        for m in games.keys():
            for num in games[m]:
                if num >= 3:
                    result += payout[m][num]
    print(f"Total win is ${result}")
    return result
#
def read(file_name, home=None):
    data = []
    res = []
    with open(file_name) as book:
        for line in book:
            ln = line.split(" - ")
            ln[-1] = ln[-1].replace('\n', '')
            for num in ln:
                res.append((int)(num))
            data.append(res)
            res = []
    name = file_name.replace('.txt', '')
    home[name]['sample_size'] = len(data)
    home[name]['len'] = len(data)
    return data
#
def frequency(name, home=None):
    res = {}.fromkeys(x for x in range(1, home[name]["range"]))
    for line in home[name]['data']:
        for num in line:
            if res[num] == None:
                res[num] = 1
            else:
                res[num] += 1
    return res
#
def parity(name, home=None):
    res = []
    string = ''
    for line in home[name]['data']:
        for num in line:
            if num % 2 == 0:
                string += '0'
            else:
                string += '1'
        res.append(string)
        string = ''
    return res
#
def parity_simplify(name, home=None):
    res = {}
    for line in home[name]['parity']:
        if line in res:
            pass
        else:
            res[line] = home[name]['parity'].count(line)
    return res
#
def probability(name, home=None):
    #name = file_name.replace('.txt', '')
    result = {}
    for k, v in home[name]['frequency'].items():
        result[k] = v / home[name]['sample_size']
    return result
#
def last_played(name, home=None):
    res = {}
    days = 0
    arr = []
    for x in range(1, home[name]['range']):
        for line in home[name]['data']:
            if x in line:
                arr.append(days)
                days = 0
            else:
                days += 1
        res[x] = arr
        arr = []
        days = 0

    return res
#
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
#
def test_all(name, r):
    print("Running ", name)
    file_name = name+".txt"
    c = 5
    if name == "lotto":
        c = 6
    Home = {
        name: {
            'range': r,
            'choice': c,
            'data': [],
            'frequency': [],
            'prob': {},
            'last_played': {},
            'sample_size': 0,
            'parity': [],
            'parity_simplify' : {},
            'default_probability': {},
            'current_probability': {},
            'len': 0,
            'group_len' : 0,
            'group_count' : {},
            'first_nums' : []
        }
    }
    Home[name]['data'] = read(file_name, Home)
    Home[name]['frequency'] = frequency(name, Home)
    Home[name]['last_played'] = last_played(name, Home)
    Home[name]['parity'] = parity(name, Home)
    Home[name]['parity_simplify'] = parity_simplify(name, Home)
    Home[name]['deault_probability'] = default_probability(name, Home)
    Home[name]['current_probability'] = current_probability(name, Home)
    Home[name]['group_count'] = group_count(name, Home)
    #for i in range(1, Home[name]['range']):
        #print(f"Number [{i}]\tFrequency: [{Home[name]['frequency'][i]}] \t Last Played: [{Home[name]['last_played'][i]}]")
    for k, v in Home[name]['group_count'].items():
        print('Position : ', k, ' : ', v)
    passTwo(name, Home)
    plays = list(combinations([x for x in range(1, Home[name]['range'])], c))
    # this is creating a list that contains all of the possible outcome for the a winning ticket.
    i = 0
    for num in plays:
        plays[i] = list(num)
        i += 1
    #print(plays)
    # this is to track how often a winning ticket repeats.
    wonRep = {}
    for t in Home[name]['data']:
        wonRep[ticket_to_string(t)] = Home[name]['data'].count(t)#count_it(name, Home, t)
    for k, v in wonRep.items():
        if v > 1:
            print("Points: ", k, " : ", v)
    l = len(plays)
    print(f"The size of ticket history is : {len(Home[name]['data'])}")
    print(f"The size of the plyable list is {l}")
    # Filter one removes all of the tickets that have won before
    Filter1 = filter_1(name, Home, plays)
    print(f"The size of the plyable list is {len(Filter1)}")
    mygroups = group_plays(name, Home)  # print to see what this is.
    return Filter1, Home, mygroups
#
def games_of_the_day():
    clear()
    day = time.strftime('%A')
    if day == "Monday":
        print(f"\t\t\t\t\t\t\t\tYou can play: |Cash5|\t|Lucky 4 Life|")
    elif day == "Tuesday" or day == "Friday":
        print(f"\t\t\t\t\t\t\t\tYou can play: |Cash5|\t|Lotto|\t|Mega Million|")
    elif day == "Wednesday" or day == "Saturday":
        print(f"\t\t\t\t\t\t\t\tYou can play: |Cash5|\t|PoweBall|")
    elif day == "Thursday":
        print(f"\t\t\t\t\t\t\t\tYou can play: |Cash5|\t|Luck 4 Life|")
    elif day == "Sunday":
        print(f"\t\t\t\t\t\t\t\tYou can play: |Cash5|\t||")
# gets input from the user.
def getPlay(n):
    play = []
    m = n
    while(m > 0):
        play.append((int)(input(f"Enter number {m}:")))
        m -= 1
    return play
#
if __name__ == '__main__':
    games_of_the_day()
    #m = check_wins()
    #n = wins(m)
    
    tests = [[[11, 20, 27, 32, 34],
                [3, 11, 12, 25, 26],
                [7, 16, 17, 28, 33],
                [8, 12, 20, 25, 32],
                [1, 4, 25, 30, 35],
                [8, 13, 18, 22, 24],
                [4, 9, 15, 16, 24],
                [1, 5, 18, 22, 24],
                [8, 10, 19, 32, 35],
                [3, 5, 16, 28, 35],
                [5, 7, 17, 30, 33],
                [3, 5, 8, 29, 34],
                [13, 14, 19, 23, 26],
                [18, 20, 22, 24, 25],
                [14, 18, 21, 24, 33],
                [4, 5, 6, 29, 35],
                [8, 9, 22, 26, 31]], 
                [[1, 9, 19, 24, 25, 34],
                [22, 29, 36, 37, 38, 39],
                [2, 10, 14, 20, 22, 29],
                [5, 8, 15, 28, 31, 39],
                [6, 12, 14, 23, 33, 38]], 
                [[2, 10, 12, 43, 45],
                [10, 11, 17, 27, 32],
                [1, 21, 22, 34, 45],
                [7, 9, 15, 31, 39],
                [2, 12, 22, 24, 26]], 
                [[5, 7, 9, 20, 57],
                [27, 32, 47, 50, 53],
                [1, 36, 44, 54, 66],
                [5, 14, 24, 25, 27],
                [7, 18, 21, 31, 40]],
                [[4, 33, 43, 53, 65],
                [4, 8, 22, 32, 58],
                [1, 15, 21, 32, 46],
                [20, 28, 33, 63, 68],
                [15, 39, 58, 63, 67]]]
    names = ["cash5", "lotto", "4life", "mega", "power"]
    ranges = [36, 45, 49, 71, 70]
    """for n in names:
        filename = n + " to play4"
        s = getTickets(filename)
        print("Tickets for ", filename)
        for i in s:
            print(i)"""
    #lst = getTickets()
    #for l in lst:
        #print(l)
    #lotto_thread = threading.Thread(target=test_lotto, args=())
    if 9 == 9:
        for x in range(len(names)):
            name = names[x]
            range_value = ranges[x]
            Filter1, Home, mygroups = test_all(name, range_value)
            #result = whole(name, Home, mygroups)
            #print_whole(result)
            test = tests[x]
            odds = []
            i = print_is_in(Filter1, test)
            odds.append([i, len(Filter1)])
            print(f"The size of Filter 1 is [{len(Filter1)}]")
            gf, not_gf = mode_filter(Filter1)
            print(f"The length of Group Format is [{len(gf)}] and not_fg is [{len(not_gf)}]")
            i = print_is_in(gf, test)
            odds.append([i, len(gf)])
            print(f"Your Chance of winning is : [{i} / {len(gf)}] = {i/len(gf)}")
            myformat = []
            notmyformat = []
            for p in gf:
                if format_(name, p):
                    myformat.append(p)
                else:
                    notmyformat.append(p)
            
            i = print_is_in(myformat, test)
            odds.append([i, len(myformat)])
            print(f"The length of Group Format is [{len(myformat)}] and notmyformat is [{len(notmyformat)}]")
            print(f"Your Chance of winning is : [{i} / {len(myformat)}] = {i/len(myformat)}")
            newx = [myformat[0]]
            c = 0
            for i in range(1, len(myformat)):
                if consecutive_common(newx[c], myformat[i]) <= 4:
                    newx.append(myformat[i])
                    c += 1
            i = print_is_in(newx, test)
            odds.append([i, len(newx), i / len(newx)])
            print("The size of newx is : ", len(newx))
            write(newx, name+" to play4")
            write(odds, name+" ODDS")
            print(print_is_in(newx, test))
            
            final = []
            for n in newx:
                state = True
                for m in Home[name]['data']:
                    if consecutive_common(n, m) >= 3 or in_common(n, m) >= 4:
                        state = False
                        break
                    else:
                        continue
                if state:
                    final.append(n)
                        
            i = print_is_in(final, test)
            odds.append([i, len(final), i / len(final)])
            print("The size of final is : ", len(final))
            write(final, name+" removed4")
            write(odds, name+" ODDS")
            print(print_is_in(final, test))