import sys
import random
import numpy as np
from queue import LifoQueue

# from playsound import playsound as ps

bst_fst_sucStack_h1 = LifoQueue()
bst_fst_sucStack_h2 = LifoQueue()
bst_fst_sucStack_h3 = LifoQueue()

arg_err_msg = 'Sorry, your input puzzle wasn\'t formatted correcty. It should be a permutation of the form: 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 _'

mhtn = {1:[0, 1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 5, 3, 4, 5, 6],
        2:[1, 0, 1, 2, 2, 1, 2, 3, 3, 2, 3, 4, 4, 3, 4, 5],
        3:[2, 1, 0, 1, 3, 2, 1, 2, 4, 3, 2, 3, 5, 4, 3, 4],
        4:[3, 2, 1, 0, 4, 3, 2, 1, 5, 4, 3, 2, 6, 5, 4, 3],
        5:[1, 2, 3, 4, 0, 1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 5],
        6:[2, 1, 2, 3, 1, 0, 1, 2, 2, 1, 2, 3, 3, 2, 3, 4],
        7:[3, 2, 1, 2, 2, 1, 0, 1, 3, 2, 1, 2, 4, 3, 2, 3],
        8:[4, 3, 2, 1, 3, 2, 1, 0, 4, 3, 2, 1, 5, 4, 3, 2],
        9:[2, 3, 4, 5, 1, 2, 3, 4, 0, 1, 2, 3, 1, 2, 3, 4],
        10:[2, 3, 3, 4, 2, 1, 2, 3, 1, 0, 1, 2, 2, 1, 2, 3],
        11:[4, 3, 2, 2, 3, 2, 1, 2, 2, 1, 0, 1, 3, 2, 1, 2],
        12:[5, 4, 3, 2, 4, 3, 2 ,1, 3, 2, 1, 0, 4, 3, 2, 1],
        13:[3, 4, 5, 6, 2, 3, 4, 5, 1, 2, 3, 4, 0, 1, 2, 3],
        14:[4, 3, 2, 1, 3, 2, 3, 4, 2, 1, 2, 3, 1, 0, 1, 2],
        15:[5, 4, 3, 4, 4, 3, 2, 3, 3, 2, 1, 2, 2, 1, 0, 1],
        16:[6, 5, 4, 3, 5, 4, 3, 2, 4, 3, 2, 1 ,3, 2, 1, 0]
        } 

goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

move_dict = {'U': -4, 'R': 1,'D': 4, 'L': -1}

def get_successors_with_memory(puzz, move_options, blank, heuristic):
    
    all_successors = {}
    hs = []
    sucs_sorted_by_h_value = []

    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for successor in all_successors.values():
        h = get_h_value(successor, heuristic)
        hs.append(h)

    sucs = list(zip(hs, all_successors.values()))
    hs.sort()
    for h in hs: 
        for suc in sucs:
            if suc[1] not in sucs_sorted_by_h_value and suc[0] == h: 
                 sucs_sorted_by_h_value.append(suc[1])
    
    sucs_sorted_by_h_value.reverse()
    return sucs_sorted_by_h_value   

def successors_with_memory(puzz, heuristic, sucStack, seen_sucs):

    move_options, blank = get_move_options(puzz)    
    sucs = get_successors_with_memory(puzz, move_options, blank, heuristic)
    
    for suc in sucs:
        if suc not in seen_sucs:
            sucStack.put(suc)
            seen_sucs.append(suc)
    return

def best_first_with_memory(puzz, heuristic, sucStack):
    
    seen_sucs = []   
    chosen_path = [] 
    
    if sucStack.empty():
        sucStack.put(puzz)
    else:
        print('The Stack has elements in it!')
        exit()

    count = 0
    while(not sucStack.empty()):
        
        next_puzz = sucStack.get()
        count += 1
        if(next_puzz == goal):
            print('Goal!')
            f = open('best_first_out.txt', 'w')                                
            for p in chosen_path:
                f.write('{}-->'.format(p))
            f.write('Number of tried nodes: {}'.format(sucStack.qsize()))
            f.close()
            break
        successors_with_memory(next_puzz, heuristic, sucStack, seen_sucs) 
    print('Number of tried nodes for {}: '.format(heuristic), count)
    return

def print_puzz(puzz):
    
    puzz = ['_' if i == 16 else i for i in puzz]

    for i in range(0, 16, 4):
        print('[  {}  {}  {}  {} ]\n'.format(puzz[i], puzz[i+1], puzz[i+2], puzz[i+3]))
    return 

def is_solvable(puzz):

    print(puzz)
    y =[]
    blank_index = 0
    for i, num in enumerate(puzz):
        if num == '_':
            y.insert(i, 16)
            blank_index = i
        else:
            y.insert(i, int(num))
    print(y, blank_index)
    count = 0
    for i in range(0, len(y)-1):
        for j in range(i, len(y)):
            if(y[i] > y[j]):
                count+=1
    print('Inversions: {}'.format(count))
    if(count%2==0 and blank_index in [0, 1, 2, 3, 8, 9, 10, 11]):
        return True
    elif(count%2==1 and blank_index in [4, 5, 6, 7, 12, 13, 14, 15]):
        return True
    return False

def get_out_of_order(puzz):
    
    out_order =[]
    oo_index  =[]
    for i in range(len(puzz)):
        if(puzz[i] == goal[i]):
            continue
        else:
            out_order.append(puzz[i])
            oo_index.append(i)
    oo = dict(zip(out_order, oo_index))
    return oo

def get_manhattan(puzz):

    h = 0
    out_order = get_out_of_order(puzz)
    for number, index in out_order.items():
        h+= mhtn[number][index]
    return h

def get_misplaced_number(puzz):
    
    out_order = get_out_of_order(puzz)
    h = len(out_order.keys())
    return h

def get_my_heuristic(puzz):

    row_is = [[1,2,3,4],  [5,6,7,8], [9,10,11,12], [13,14,15,16]]
    col_is = [[1,5,9,13], [2,6,10,14], [3,7,11,15], [4,8,12,16]]

    h = 0
    for i in range(4):
        for j in range(4):
            if puzz[(i*4)+j] != goal[i]:
                if puzz[(i*4)+j] not in row_is[i]:
                    h +=1
                if puzz[(i*4)+j] not in col_is[j]:
                    h +=1
    return h


def get_h_value(puzz, heuristic):
    
    if heuristic == 'mhtn':
        h = get_manhattan(puzz) 
    elif heuristic == 'tiles': 
        h = get_misplaced_number(puzz)
    else:
        h = get_my_heuristic(puzz)
    return h

def get_move_puzz(puzz, direction, blank):

    new_puzz = puzz.copy()
    swap_index = move_dict[direction]+blank
    temp = new_puzz[swap_index]
    new_puzz[swap_index] = 16
    new_puzz[blank] = temp
    return new_puzz

def get_move_options(puzz):
    
    index_of_blank = [i for i, x in enumerate(puzz) if x == 16]
    blank = index_of_blank[0]
    move_options = {'U': True, 'R': True, 'D': True, 'L': True} 
    if(blank != 6 or blank != 7 or blank != 10 or blank != 11):
        if(blank <=3):
            move_options['U'] = False
        elif(blank >=12):
            move_options['D'] = False
        if(blank in [3, 7, 11, 15]):
            move_options['R'] = False
        elif(blank in [0, 4, 8, 12]):
            move_options['L'] = False
    return move_options, blank

def get_successors(puzz, move_options, blank, heuristic):
    
    all_successors = {}
    hs = []
    sucs_sorted_by_h_value = []

    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for successor in all_successors.values():
        h = get_h_value(successor, heuristic)
        hs.append(h)

    sucs = list(zip(hs, all_successors.values()))

    hs.sort()
    for h in hs: 
        for suc in sucs:
            if suc[1] not in sucs_sorted_by_h_value and suc[0] == h: 
                 sucs_sorted_by_h_value.append(suc[1])
    
    return sucs_sorted_by_h_value[0]   

def successors(puzz, heuristic, sucStack):

    move_options, blank = get_move_options(puzz)    
    suc = get_successors(puzz, move_options, blank, heuristic)
    
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
        count += 1
        chosen_path.append(next_puzz)
        if(count == 100000):
            print('This puzzle was not solved in 100000 turns')
            return
        if(next_puzz == goal):
            print('Goal!')
            for p in chosen_path:
                print('\n{}-->'.format(p))
            return
        successors(next_puzz, heuristic, sucStack, ) 
    print('Number of tried nodes for {}: '.format(heuristic), count)
    return

def a_star(puzz, heuristic):
    
    seen_sucs = []
    chosen_path = []
    current_g_value = 0
    parents = []
    
    init_h_value = get_manhattan(puzz)
    chosen_path.append(puzz) # expanded?, depth, heuristic, f(n) = depth+heuristic, puzzle
    seen_sucs.append((True, current_g_value, init_h_value, current_g_value+init_h_value, puzz))
    
    count = -1
    while(len(chosen_path) !=0):
          
        next_puzz = chosen_path[current_g_value] 
        current_g_value = len(chosen_path) 
        count += 1
        
        count_limit = 100000
        if(count == count_limit):
            print('This puzzle was not solved in {} turns'.format(count_limit))
            return
        if(next_puzz == goal):
            print('Goal!')                            
            for p in chosen_path:
                print_puzz(p)
                print()
            print('A* with {} heuristic solved this badboy after expanding {} puzzle configurations (nodes)'.format(heuristic, count))
            return
        
        else:
            chosen_path, seen_sucs, parents, current_g_value = successors_a_star(next_puzz, heuristic, seen_sucs, chosen_path, parents, current_g_value) 
    return

def get_successors_a_star(puzz, move_options, blank, heuristic):
    
    hs =[]
    all_successors = {}
    for direction, can_move in move_options.items():
        if(can_move):
            all_successors[direction] = get_move_puzz(puzz, direction, blank)

    for successor in all_successors.values():
        h = get_h_value(successor, heuristic)
        hs.append(h)

    sucs = list(zip(hs, all_successors.values()))
    return sucs, hs

def successors_a_star(puzz, heuristic, seen_sucs, chosen_path, parents, g):

    move_options, blank = get_move_options(puzz)    
    sucs, hs = get_successors_a_star(puzz, move_options, blank, heuristic)
    
    seen_sucs, parents = update_explored_list(sucs, seen_sucs, chosen_path, parents, hs, g)
    chosen_successor, seen_sucs, chosen_path, g = choose_succesor(chosen_path, seen_sucs, parents, g)
    
    if chosen_successor == []:
        print('No successors!')
        exit()
    else:
        chosen_path.append(chosen_successor)
    return chosen_path, seen_sucs, parents, g

def update_explored_list(sucs, seen_sucs, chosen_path, parents, hs, g):

    for suc in sucs:
        found = False
        suc_h = suc[0]
        for j in range(len(seen_sucs)):
            if seen_sucs[j][4] == suc[1]:
                found = True
                other_f = seen_sucs[j][3]
                if g+suc_h < other_f: # if we found a cheaper way to get to this node? shouldn't happen
                    for rel in parents:
                        if rel[0] == suc:
                            print('error')
                            exit()
                    continue
                            
        if not found:
            new_node = (False, g, suc_h, suc[0]+g, suc[1])
            seen_sucs.append(new_node)
            parent_child = (chosen_path[-1], suc[1])
            parents.append(parent_child)

    seen_sucs =sorted(seen_sucs, key=lambda x: x[3])
    return seen_sucs, parents
 

def choose_succesor(chosen_path, seen_sucs, parents, g):

    chosen_successor = []
    
    for i in range(len(seen_sucs)):
        
        if  seen_sucs[i][4] not in chosen_path and seen_sucs[i][0] == False:
            g = seen_sucs[i][1]
            chosen_path = []
            parent_child = [pair for pair in parents if pair[1] == seen_sucs[i][4]]
            
            while(len(parent_child) > 0):
                parent = parent_child[0][0]
                chosen_path.insert(0, parent)
                parent_child = [pair for pair in parents if pair[1] == parent]
                
            update_tuple = (True, seen_sucs[i][1], seen_sucs[i][2], seen_sucs[i][3], seen_sucs[i][4])
            seen_sucs[i] = (update_tuple) 
            chosen_successor = seen_sucs[i][4]
            break

    return chosen_successor, seen_sucs, chosen_path, g

def main():
    
    if len(sys.argv) != 17: 
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
    puzz = [16 if i == '_' else int(i) for i in puzz]
 
    print("First trying best first search without an explored list...")
    best_first(puzz, 'mhtn', bst_fst_sucStack_h1)
    best_first(puzz, 'tiles', bst_fst_sucStack_h2)
    best_first(puzz, 'my_h', bst_fst_sucStack_h3)
    
    # print("Now trying best first search with explored list (doesn't print the path)")
    # best_first_with_memory(puzz, 'mhtn', bst_fst_sucStack_h1)
    # best_first_with_memory(puzz, 'tiles', bst_fst_sucStack_h2)
    # best_first_with_memory(puzz, 'my_h', bst_fst_sucStack_h3)

    print("Now trying A *.................")
    a_star(puzz, 'mhtn')
    a_star(puzz, 'tiles')
    a_star(puzz, 'my_h')

    return     

if __name__ == "__main__":
    main()