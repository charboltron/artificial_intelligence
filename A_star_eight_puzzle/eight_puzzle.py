import sys
import numpy as np
from queue import LifoQueue
sucStack = LifoQueue()

"""Known best first solutions: 
   2 1 3 5 4 6 7 _ 8
   _ 5 2 1 8 3 4 7 6
"""

mhtn = {1:[0, 1, 2, 1, 2, 3, 2, 3, 4],
        2:[1, 0, 1, 2, 1, 2, 2, 2, 3],
        3:[2, 1, 0, 3, 2, 1, 4, 3, 2],
        4:[1, 2, 3, 0, 1, 2, 1, 2, 3],
        5:[2, 1, 2, 1, 0, 1, 2, 1, 2],
        6:[3, 2, 1, 2, 1, 0, 3, 2, 1],
        7:[2, 3, 4, 1, 2, 3, 0, 1, 2],
        8:[3, 2, 3, 2, 1, 2, 1, 0, 1],
        0:[4, 3, 2, 3, 2, 1, 2, 1, 0]
        } 

goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
seen_sucs = []

move_dict = {'U': -3, 'R': 1,'D': 3, 'L': -1}

def print_puzz(puzz):
    
    for i in range(0, 9, 3):
        print('[  {}  {}  {}  ]\n'.format(puzz[i], puzz[i+1], puzz[i+2]))
    return 

def is_solvable(puzz):

    y = [ord(i)-48 for i in puzz if ord(i) in range(48, 57)]
    # print(y)
    count = 0
    for i in range(0, len(y)-1):
        for j in range(i, len(y)):
            if(y[i] > y[j]):
                # print('Inversion: {} and {}'.format(y[i], y[j]))
                count+=1
    # print(count)
    if(count%2==1):
        print('Inversions: {}'.format(count))
        return False
    return True

def get_out_of_order(puzz):
    
    out_order =[]
    oo_index  =[]
    for i in range(len(puzz)):
        if(puzz[i] == goal[i]):
            continue
            # print('match at {}'.format(puzz[i]))
        else:
            out_order.append(puzz[i])
            oo_index.append(i)
    # print(out_order)
    oo = dict(zip(out_order, oo_index))
    # print('out of order: {}'.format(oo))
    return oo

def manhattan(puzz):

    h = 0
    out_order = get_out_of_order(puzz)
    for number, index in out_order.items():
        h+= mhtn[number][index]
    return h

def get_move_puzz(puzz, direction, blank):

    new_puzz = puzz.copy()
    swap_index = move_dict[direction]+blank
    # print(swap_index)
    temp = new_puzz[swap_index]
    new_puzz[swap_index] = 0
    new_puzz[blank] = temp
    return new_puzz

def get_move_options(puzz):
    
    index_of_blank = [i for i, x in enumerate(puzz) if x == 0]
    blank = index_of_blank[0]
    # print('index of space = {}'.format(blank))
    move_options = {'U': True, 'R': True, 'D': True, 'L': True} 
    if(blank != 4):
        if(blank <=2):
            move_options['U'] = False
        elif(blank >=6):
            move_options['D'] = False
        if(blank in [2, 5, 8]):
            move_options['R'] = False
        elif(blank in [0, 3, 6]):
            move_options['L'] = False
    return move_options, blank

def get_successors(puzz, move_options, blank):
    
    all_successors = {}
    hs = []
    sucs_sorted_by_h_value = []

    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for move, successor in all_successors.items():
        h = manhattan(successor)
        hs.append(h)
        print(move)
        # print('h = {}'.format(h))
        print(' -----------')
        print_puzz(successor)

    sucs = list(zip(hs, all_successors.values()))
    # for s in sucs:
    #     print(s)
    # print(all_successors)
    hs.sort()
    for h in hs: 
        for suc in sucs:
            if suc[1] not in sucs_sorted_by_h_value and suc[0] == h: 
                 sucs_sorted_by_h_value.append(suc[1])
    
    # print('hs = {}'.format(hs))
    sucs_sorted_by_h_value.reverse()
    return sucs_sorted_by_h_value   

def successors(puzz):

    move_options, blank = get_move_options(puzz)
    # print('move options = {}'.format(move_options))
    sucs = get_successors(puzz, move_options, blank)
    # print('sucs in rev order of h: {}'.format(sucs))
    
    for suc in sucs:
        if suc not in seen_sucs:
            sucStack.put(suc)
            seen_sucs.append(suc)
    # print('seen sucs: {}'.format(seen_sucs))
    return

def best_first(puzz):
    
    chosen_path = []
    h = manhattan(puzz) #calculate heuristic value
    # print('This puzzle has mhtn(h) = {}'.format(h))
    sucStack.put(puzz)
    count = 0
    while(not sucStack.empty()):
        
        next_puzz = sucStack.get()
        print('choosing: ')
        print_puzz(next_puzz)
        count += 1
        print('Round {}. looking at moves. Height of stack: {}'.format(count, sucStack.qsize()))
        chosen_path.append(next_puzz)
        if(next_puzz == goal):
            print('Goal!')
            f = open('best_first_out.txt', 'w')                                
            for p in chosen_path:
                f.write('{}-->'.format(p))
            f.write('Number of tried nodes: {}'.format(sucStack.qsize()))
            f.close()
            break
        successors(next_puzz) 

    return

def a_star(puzz):
    pass

def my_heuristic(puzz):
    pass

def main():
    
    if len(sys.argv) != 10: 
        print('Sorry, your input puzzle wasn\'t formatted correcty. It should be a permutation of the form: 1 2 3 4 5 6 7 8 _')
        exit()
    puzz = [arg for arg in sys.argv[1:]]
    # print('Input: {}'.format(puzz))
    print("Initial Input Puzzle:")
    print_puzz(puzz)

    if(is_solvable(puzz)==False):
        print('Not solvable')
        exit()
    else:
        print('Solvable')
    
    puzz = [0 if i == '_' else int(i) for i in puzz]
    if(puzz == goal):
        print('Goal!')

    best_first(puzz)
    a_star(puzz)
    my_heuristic(puzz)

    return     

if __name__ == "__main__":
    main()