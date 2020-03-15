import sys
import random
import numpy as np
from queue import LifoQueue

bst_fst_sucStack_h1 = LifoQueue()
bst_fst_sucStack_h2 = LifoQueue()
bst_fst_sucStack_h3 = LifoQueue()
a_star_sucStack_h1 = LifoQueue()
a_star_sucStack_h2 = LifoQueue()
a_star_sucStack_h3 = LifoQueue()
seen_sucs1 = {}
seen_sucs2 = {}
seen_sucs3 = {}

"""Known best first solutions: 
   2 1 3 5 4 6 7 _ 8
   _ 5 2 1 8 3 4 7 6
"""

arg_err_msg = 'Sorry, your input puzzle wasn\'t formatted correcty. It should be a permutation of the form: 1 2 3 4 5 6 7 8 _'

mhtn = {1:[0, 1, 2, 1, 2, 3, 2, 3, 4],
        2:[1, 0, 1, 2, 1, 2, 2, 2, 3],
        3:[2, 1, 0, 3, 2, 1, 4, 3, 2],
        4:[1, 2, 3, 0, 1, 2, 1, 2, 3],
        5:[2, 1, 2, 1, 0, 1, 2, 1, 2],
        6:[3, 2, 1, 2, 1, 0, 3, 2, 1],
        7:[2, 3, 4, 1, 2, 3, 0, 1, 2],
        8:[3, 2, 3, 2, 1, 2, 1, 0, 1],
        9:[4, 3, 2, 3, 2, 1, 2, 1, 0]
        } 

goal = [1, 2, 3, 4, 5, 6, 7, 8, 9]

move_dict = {'U': -3, 'R': 1,'D': 3, 'L': -1}

def print_initial_puzz(puzz):

    f = open('out.txt', 'a')                                
    f.write('Current Puzzle Configuration:\n')
    puzz = ['_' if i == 9 else i for i in puzz]
    for i in range(0, 9, 3):
        f.write('[  {}  {}  {}  ]\n\n'.format(puzz[i], puzz[i+1], puzz[i+2]))
    f.close()

def print_puzzle_info(algo, heur):
    f = open('out.txt', 'a')   
    f.write('\n\nAlgorithm: {}  Heuristic: {}\n'.format(algo, heur))
    f.close()

def print_puzz(puzz):
    
    puzz = ['_' if i == 9 else i for i in puzz]

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

    f = open('out.txt', 'a')                                
    f.write('Number of Inversions: {}'.format(count))
    f.close()
    print('Inversions: {}'.format(count))
    if(count%2==1):
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

def get_manhattan(puzz):

    h = 0
    out_order = get_out_of_order(puzz)
    for number, index in out_order.items():
        h+= mhtn[number][index]
    # print('manhattan distance total: {}'.format(h))
    return h

def get_misplaced_number(puzz):
    
    out_order = get_out_of_order(puzz)
    h = len(out_order.keys())
    # print('number of misplaced tiles: {}'.format(h))
    return h

def get_my_heuristic(puzz):

    row_is = [[1,2,3], [4,5,6], [7,8,9]]
    col_is = [[1,4,7], [2,5,8], [3,6,9]]

    h = 0
    # print_puzz(puzz)
    tiles_out_of_row = 0 
    tiles_out_of_col = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if puzz[(i*3)+j] != goal[i]:
                if puzz[(i*3)+j] not in row_is[i]:
                    # print('out of row!',(puzz[(i*3)+j]))
                    tiles_out_of_row +=1
                if puzz[(i*3)+j] not in col_is[j]:
                    # print('out of col!',(puzz[(i*3)+j]))
                    tiles_out_of_row +=1
    h += tiles_out_of_row+tiles_out_of_col
    # print('my heuristic calculated:', h)
    return h


def get_h_value(puzz, heuristic):
    
    if heuristic == 'mhtn':
        h = get_manhattan(puzz) #calculate heuristic value
    elif heuristic == 'tiles': 
        h = get_misplaced_number(puzz)
    else:
        h = get_my_heuristic(puzz)
    return h

def get_move_puzz(puzz, direction, blank):

    new_puzz = puzz.copy()
    swap_index = move_dict[direction]+blank
    # print(swap_index)
    temp = new_puzz[swap_index]
    new_puzz[swap_index] = 9
    new_puzz[blank] = temp
    return new_puzz

def get_move_options(puzz):
    
    index_of_blank = [i for i, x in enumerate(puzz) if x == 9]
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

def get_successors(puzz, move_options, blank, heuristic):
    
    all_successors = {}
    hs = []
    sucs_sorted_by_h_value = []

    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for move, successor in all_successors.items():
        h = get_h_value(successor, heuristic)
        hs.append(h)
        # print('if move: {} h = {} \n -----------'.format(move, h))
        # print_puzz(successor)

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
    # sucs_sorted_by_h_value.reverse()
    return sucs_sorted_by_h_value[0]   

def successors(puzz, heuristic, sucStack):

    move_options, blank = get_move_options(puzz)    
    suc = get_successors(puzz, move_options, blank, heuristic)
    # print('move options = {}'.format(move_options))
    # print('best successor: {}'.format(suc))
    
    sucStack.put(suc)
    return

def best_first(puzz, heuristic, sucStack):
    
    chosen_path = [] 
    
    if sucStack.empty():
        sucStack.put(puzz)
    else:
        print('The Stack has elements in it!')
        exit()

    count = -1
    while(not sucStack.empty()):
        
        next_puzz = sucStack.get()
        # print('choosing: ')
        # print_puzz(next_puzz)
        count += 1
        # print('Round {}. looking at moves. Height of stack: {}'.format(count, sucStack.qsize()))
        chosen_path.append(next_puzz)
        if(count == 10000):
            print('This puzzle was not solved in 1000 turns')
            f = open('out.txt', 'a')
            f.write('Path to Goal State (9 is the blank space):\n')                   
            for p in range(0, 30):
                f.write('\n{}-->'.format(chosen_path[p]))
            f.write('....\nBest First search failed to solved this puzzle in under 10,000 moves using the {} heuristic'.format(heuristic))
            f.close()
            return
        if(next_puzz == goal):
            print('Goal!')
            f = open('out.txt', 'a')
            f.write('Path to Goal State (9 is the blank space):\n')                                
            for p in chosen_path:
                f.write('\n{}-->'.format(p))
            f.write('Number of tried nodes: {}'.format(count))
            f.close()
            return
        successors(next_puzz, heuristic, sucStack, ) 
    print('Number of tried nodes for {}: '.format(heuristic), count)
    return

def a_star(puzz, heuristic, sucStack, seen_sucs):
    
    final_fs = []
    chosen_path = []
    current_g_value = 0

    if sucStack.empty():
        sucStack.put(puzz)
    else:
        print('The Stack has elements in it!')
        exit()
    count = -1
    while(not sucStack.empty()):
        
        next_puzz = sucStack.get()
        print('choosing: ')
        print_puzz(next_puzz)
        count += 1
        # print('Round {}. looking at moves. Height of stack: {}'.format(count, sucStack.qsize()))
        while(len(chosen_path) > current_g_value):
            print('Pruning puzzle')
            pruned_puzzle = chosen_path[len(chosen_path)-1]
            chosen_path.remove(pruned_puzzle)
        if next_puzz not in chosen_path:
            chosen_path.append(next_puzz)
        else: 
            print('Next puzzle already in path!')
            exit()
        print('Chosen path with next puzzle: {} length = {} '.format(chosen_path, len(chosen_path)))
        current_g_value = len(chosen_path)
        if current_g_value not in seen_sucs: 
            seen_sucs[current_g_value] = []            
        count_limit = 30
        if(count == count_limit):
            print('This puzzle was not solved in {} turns'.format(count_limit))
            f = open('out.txt', 'a')
            f.write('Path to Goal State (9 is the blank space):\n')                   
            for p in range(len(chosen_path)):
                f.write('\n{}-->'.format(chosen_path[p]))
            f.write('....\nA* search failed to solved this puzzle in under {} moves using the {} heuristic'.format(count_limit, heuristic))
            f.close()
            return
        if(next_puzz == goal):
            print('Goal!')
            f = open('out.txt', 'a')
            f.write('Path to Goal State (9 is the blank space):\n')                                
            for p in chosen_path:
                f.write('\n{}-->'.format(p))
            f.write('Number of tried nodes: {}'.format(count))
            f.close()
            return
        else:
            current_g_value = successors_a_star(next_puzz, heuristic, sucStack, seen_sucs, chosen_path, final_fs, current_g_value) 

    print('Number of tried nodes for {}: '.format(heuristic), count)
    return

def get_successors_a_star(puzz, move_options, blank, heuristic):
    
    all_successors = {}
    hs = []
    sucs_sorted_by_h_value = []

    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for successor in all_successors.values():
        h = get_h_value(successor, heuristic)
        hs.append(h)
        # print('if move: {} h = {} \n -----------'.format(move, h))
        # print_puzz(successor)

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
    hs.reverse()
    return sucs_sorted_by_h_value, hs   

def successors_a_star(puzz, heuristic, sucStack, seen_sucs, chosen_path, final_fs, g):

    move_options, blank = get_move_options(puzz)    
    sucs, hs = get_successors_a_star(puzz, move_options, blank, heuristic)
    # print('move options = {}'.format(move_options))
    # print('sucs in rev order of h: {}'.format(sucs))
    
    fn = []
    print('g_value now = ', g)
    print('\n   Successors: ', sucs)
    
    suc_list = []
    for k in seen_sucs.keys():
        for l in seen_sucs[k]:
            if l in suc_list:
                print('???????????????????') #this shouldn't happen
                exit()
            else:
                suc_list.append(l)

    for i, suc in enumerate(sucs):
        this_h = hs[i]
        # print('the master suc_list', suc_list)
        if suc in suc_list:
            other_g = [k for k, v in seen_sucs.items() if suc in seen_sucs[k]]
            if g < other_g[0]: #this shouldn't happen
                print("-------------------??")
                exit()
                seen_sucs[g].append(suc) 
            else: 
                print("\nfound an earlier path with lower g value at level: ", other_g[0])
                print(suc)
                f_val = (other_g[0], this_h, suc)
                fn.append(f_val)
                continue
        else:
            print('Not found list of seen sucs')
            f_val = (g, this_h, suc)
            fn.append(f_val) 
            print('Adding to Seen Sucs {}\n'.format(suc))
            seen_sucs[g].append(suc)

    print('List of f(n) values w/ puzzles: ',fn)
    sorted_fs =sorted(fn, key=lambda x: x[0]+x[1])
    for i in sorted_fs:
        f = (i[0]+i[1], i[2])
        if f not in final_fs:
            final_fs.append(f)
    
    final_fs =sorted(final_fs, key=lambda x: x[0])
    print('\nsorted gs + hs = ', sorted_fs)
    print('final fs       = ', final_fs)
    chosen_successor = choose_succesor(sorted_fs, final_fs, chosen_path, seen_sucs, sucStack, g)
    if chosen_successor == []:
        print('No Successors!')
        exit()
    else:
        sucStack.put(chosen_successor)
    return g

def choose_succesor(sorted_fs, final_fs, chosen_path, seen_sucs, sucStack, g):

    chosen_successor = []
    successor_chosen = False
    i = 0
    while(not successor_chosen):
        if (final_fs[i][1] not in chosen_path):
            chosen_successor = final_fs[i][1]
            for x in sorted_fs:
                if chosen_successor == x[2]:
                    g = x[2]

            print('\nRewinding g! g now = {}\n'.format(g))
            print('Returning to puzzle',final_fs[i][1])
            successor_chosen = True
        else: 
            i+=1
            if i == len(final_fs):
                for j in range(4):
                    chosen_successor = final_fs[j][1]
                    if chosen_successor not in chosen_path:
                        successor_chosen = True            
                        break
                    else:
                        print('already in path')
    return chosen_successor

def main():
    
    if len(sys.argv) != 10: 
        print(arg_err_msg)
        exit()
    puzz = [arg for arg in sys.argv[1:]]
    print("Initial Input Puzzle:")
    print_puzz(puzz)
    if(is_solvable(puzz)==False):
        print('Not solvable')
        exit()
    else:
        print('Solvable')
    puzz = [9 if i == '_' else int(i) for i in puzz]

    f = open('out.txt', 'w')                                
 
    print_initial_puzz(puzz)
    # print_puzzle_info('Best First Search', 'Manhattan')
    # best_first(puzz, 'mhtn', bst_fst_sucStack_h1)
    print_puzzle_info('Best First Search', 'Misplaced Tiles')
    best_first(puzz, 'tiles', bst_fst_sucStack_h2)
    print_puzzle_info('Best First Search', 'My Heuristic')
    best_first(puzz, 'my_h', bst_fst_sucStack_h3)

    print_puzzle_info('A*', 'Manhattan')
    a_star(puzz, 'mhtn', a_star_sucStack_h1, seen_sucs1)

    f.close()
    return     

if __name__ == "__main__":
    main()