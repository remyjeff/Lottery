class node:
    def __init__(self, val):
        self.value = val
        self.right = NULL
        self.left = NULL
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
    home['lotto']['sample_size'] = len(data)
    return data
#
def frequency(name, home=None):
    res = {}.fromkeys(x for x in range(45))
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
def last_played(file_name, home=None):
    res = {}
    days = 0
    arr = []
    for x in range(home[name]['range']):
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
def print_data(mydict):
    for num in mydict['lotto']['data']:
        print(num, end="\n")
    print("\n")
#
def print_freq(mydict):
    for k, v in mydict['lotto']['frequency'].items():
        print(k, ' : ', v, end="\n")
    print("\n")

def print_parity(mydict):
    for num in mydict['lotto']['parity']:
        print(num, end="\n")
    print("\n")
#
def print_parity_simplify(mydict):
    sum = 0
    for k, v in mydict['lotto']['parity_simplify'].items():
        print(k, ' : ', v, end="\n")
        sum += v
    print("the length is ", len(mydict['lotto']['parity_simplify']), " and the sum is ", sum)
#
def print_last_played(mydict):
    for k, v in mydict['lotto']['last_played'].items():
        print(k, ' : ', v, end="\n")
    print("\n")
#
if __name__ == '__main__':
    file_name = 'lotto.txt'
    name = file_name.replace('.txt', '')
    Home = {
        'lotto': {
            'range': 45,
            'choice': 6,
            'data': [],
            'frequency': [],
            'prob': {},
            'last_played': {},
            'sample_size': 0,
            'parity': [],
            'parity_simplify' : {}
        }
    }
    Home['lotto']['data'] = read(file_name, Home)
    #Home['lotto']['sample_size'] = len(Home['lotto']['data'])
    Home['lotto']['frequency'] = frequency(name, Home)
    #Home['lotto']['prob'] = probability(name, Home)
    Home['lotto']['last_played'] = last_played(name, Home)
    Home['lotto']['parity'] = parity(name, Home)
    Home['lotto']['parity_simplify'] = parity_simplify(name, Home)
    print_data(Home)
    print_freq(Home)
    print_parity(Home)
    print_parity_simplify(Home)
    print_last_played(Home)
    #print(Home)




