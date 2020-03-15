#%%
import sys
import random 
import math
# import numpy as np
# import matplotlib.pyplot as plt

test_boards = [[2,4,7,4,8,5,5,2],[3,2,7,5,2,4,1,1],[2,4,4,1,5,1,2,4],[3,2,5,4,3,2,1,3]]

#constants/twiddle factors
num_iterations = 10000

def print_board(board):

   for i in range(8, 0, -1):
        print('\n')
        for j in range(8):
            if board[j] == i:
                print(u'  \u2655  ',end='')
            else:
                print(' ___ ', end='')

def test():
    fscores=[]
    for board in test_boards:
        fscore = get_fscore(board)
        print('fitness: ', fscore)
        fscores.append(fscore)
    fprobs = fitprobs(4, fscores)
    print(fprobs)

def goal_state(board):

    if get_fscore(board) == 28:
        return True
    return False

def randomize (board, n): 
    for i in range(n):  
        queens = random.randint(1,8)  
        board[i] = queens 
    return board 

population = []

def generate_population(population_size):

    population = []
    for _ in range(population_size):
        board = [0,0,0,0,0,0,0,0] 
        n = len(board) 
        randomize(board, n)
        population.append(board) 
    return population

def get_fscore(board):
    
    fitness = 28
    for i in range(len(board)-1):
        queen = i+1
        # print(f'\nThis queen: ({queen}, {board[i]})')
        # print('Other queens: ', end='')
        for j in range(i+1, len(board)):
            # is_attack = ''
            other_queen = j+1
            if(board[i] == board[j]):
                fitness -= 1
                # is_attack = '<-A!'
            elif abs((board[i] - board[j])/((queen)-(other_queen))) == 1:
                fitness -= 1
                # is_attack = '<-A!'
            # print(f'({other_queen}, {board[j]}){is_attack}, ', end='')
    
    return fitness

def get_probs(population):

    fscores = []    
    for i in range(len(population)):
        fscore = get_fscore(population[i])
        fscores.append(fscore)
    fprobs = fitprobs(len(population), fscores)
    
    return fscores, fprobs

def fitprobs(pop_size, fs):

    denom = 0
    probs = []
    for i in range(pop_size):
        denom+=fs[i]
    if(denom > 0):
        for i in range(pop_size):
            s_i = fs[i]/denom 
            probs.append(s_i)
    else: 
        print("Error: Denom !>0 !")
        exit()
    return probs

def get_avg_fitness(fs, pop_size):

    avg = 0
    for i in range(pop_size):
        avg+=fs[i]
    avg = avg/pop_size
    return avg


def cull_population(d, initial_popsize, pop_size, population): 

    # print("population size before culling: ", len(d))
    cull_size = pop_size-initial_popsize
    
    d = sorted(d, key=lambda x: x[0])
    for i in range(cull_size):
        temp = d[i][1]
        for j in range(len(population)):
            if population[j] == temp:
                # print(f'deleting j = {population[j]}') 
                del population[j]
                break
        del d[i]
    # print("population size after culling: ", len(d))
    return d, pop_size-cull_size, population

def fitness_proportionate_selection(d):

    sum_of_fitness = 0.0
    bins = []
    for i in d:
        sum_of_fitness+=i[0]
    # print(sum_of_fitness)
    # print(d)
    prev_prob = 0.0
    d = sorted(d, key=lambda x: x[0])
    for i in range(len(d)): 
        # print(d[i][0])
        if (i+1) == len(d):
            right_range = 1.0
        else:
            right_range =  prev_prob + d[i][0] 
        bins.append([prev_prob, right_range])
        prev_prob += d[i][0]
    # for bin in bins:
    #     print(bin)
    return bins

def select_from_population(bins, d):

    mom, dad = [],[]

    cnt = 0
    while(mom == [] or dad == []):
        cnt+=1
        x = random.randint(0, 100)/100
        y = random.randint(0, 100)/100
        x = .9999999 if x > .99 else x 
        x = .0000001 if x < 0.01 else x
        y = .9999999 if y > .99 else y 
        y = .0000001 if y < 0.01 else y
        # while(y == x):
        #     y = random.randint(0, 100)/100
        for i, bin in enumerate(bins):
            # print(bin)
            if x >= bin[0] and x <= bin[1]:
                mom = d[i]
            if y >= bin[0] and y <= bin[1]:
                dad = d[i]
        if cnt == 1000:
            print("wtf")
            print(mom, dad)
            exit()
    if mom == [] or dad == []:
        print("Empty list after selection! Exiting.")
        print(x, y, mom, dad)
        exit()

    return mom, dad


def breed(d):
    
    bins = fitness_proportionate_selection(d)
    mom, dad = select_from_population(bins, d)
    # print(f'mom: {mom}, dad: {dad}')

    split = random.randint(1,7)
    # print(f'split = {split}')
    
    mom_genes_first = mom[1][0:split]
    dad_genes_first = dad[1][split:]
    dad_genes_secnd = dad[1][0:split]
    mom_genes_secnd = mom[1][split:]
    # print(f'{mom_genes_first} , {dad_genes_first}')
    # print(f'{dad_genes_secnd} , {mom_genes_secnd}')
    
    first_born = [0,0,0,0,0,0,0,0]
    secnd_born = [0,0,0,0,0,0,0,0]
    for i in range(8):
        if i < split:
            first_born[i] = mom_genes_first[i]
            secnd_born[i] = dad_genes_secnd[i]
        else: 
            first_born[i] = dad_genes_first[split-i]
            secnd_born[i] = mom_genes_secnd[split-i]
    # print(f'M: {mom}, D: {dad}, C1: {first_born}, C2: {secnd_born}') 
    
    return first_born, secnd_born

def mutate(c1, c2, mutation_thresh):

    m1 = random.randint(0, 100)/100
    m2 = random.randint(0, 100)/100
    if m1 >= mutation_thresh:
        queen_to_mutate = random.randint(0, 7)
        c1[queen_to_mutate] = random.randint(1, 8)  
    if m2 >= mutation_thresh:
        queen_to_mutate = random.randint(0, 7)
        c2[queen_to_mutate] = random.randint(1, 8)
    return c1, c2

def genetic_eight_queens(pop_size, m):    
        
    f = open('out.txt', 'w')    
    print(f'\nBegin up to {num_iterations} iterations: Breeding...')
    avg_fitness_to_pop = []
    population = generate_population(pop_size)
    initial_pop_size = pop_size
    # print(fs)
    fittest = 0.0
    board = []
    fs, probs = get_probs(population)
    d = list(zip(probs, population))
    for i in range(num_iterations):
        if initial_pop_size < pop_size: 
            d, pop_size, population = cull_population(d, initial_pop_size, pop_size, population)  
        if i%100==0:
            # print(pop_size)
            print(f'i:..{i} ')
            f.write(f'\nfittest member of population at iteration {i}: {d[len(d)-1]}. Score: {fittest}')
            # print(f'fittest = {fittest} board: {board}')
        # print(len(population))
        fs, probs = get_probs(population)
        d = list(zip(probs, population))
        # print(fs)
        avg_fitness_to_pop.append((i, get_avg_fitness(fs, pop_size)))
        for k in range(len(d)):
            if fs[k] > fittest:
                fittest = fs[k]
                board = d[k][1]

        d = sorted(d, key=lambda x: x[0])
        
        child1, child2 = breed(d)
        child1, child2 = mutate(child1, child2, m)
        if goal_state(child1):
            print(f'\nGoal State has been found! After: {i} iterations.\n')
            print(f'This is the configuration of queens found {child1}\n')
            print_board(child1)
            return avg_fitness_to_pop, i
        elif goal_state(child2):
            print(f'\nGoal State has been found! After: {i} iterations.\n')
            print(f'This is the configuration of queens found {child2}\n')
            print_board(child2)
            return avg_fitness_to_pop, i

        population.append(child1)
        population.append(child2)              
        pop_size+=2      

    print(f'No Goal State was found after {i} iterations.\n')
    return avg_fitness_to_pop, num_iterations

def main():

    # test()   
    p = input("Please enter initial population size in the range (10, 1000): ")
    if int(p) < 10 or int(p) > 1000:
        print('You entered a bad population number. Exiting')
        exit()
    pop_size = int(p)
    
    m = input("Please enter mutation rate as a percentage in the range (0, 100): ")
    if int(m) < 0 or int(m) > 100:
        print('You entered a bad mutation percentage. Exiting')
        exit()
    mutation_thresh = (100 - int(m))/100
    mutation_rate = int(m)

    #breeding frequencies
    avg1, is_til_goal = genetic_eight_queens(pop_size, mutation_thresh)

    print('\n')

if __name__ == "__main__":
    main()


# %%
