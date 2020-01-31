import random

move_dict = {'Up': -3, 'Right': 1,'Down': 3, 'Left': -1}

def print_world(world):

    for i in range(0, 9, 3):
        print('[  {}  {}  {}  ]\n'.format(world[i], world[i+1], world[i+2]))
    return 

def generate_worlds():

    world1 = [0 for i in range(0, 9)]
    world3 = [0 for i in range(0, 9)]
    world5 = [0 for i in range(0, 9)]
    random_1 = random.randint(0, 8)
    randomlist_3 = []
    randomlist_5 = []

    for i in range(0,3):
        n = random.randint(0,8)
        while(n in randomlist_3):
            n = (n+1)%9      
        randomlist_3.append(n)
    
    for i in range(0,5):
        n = random.randint(0,8)
        while(n in randomlist_5):
            n= (n+1)%9            
        randomlist_5.append(n)

    world1[random_1] = 1
    for i in randomlist_3:
        world3[i] = 1
    
    for i in randomlist_5:
        world5[i] = 1

    return world1, world3, world5

def reflex_world(dirtcount, reflex_rules, world):

    spawn_location = random.randint(0, 8)
    world_still_dirty = dirtcount
    location = spawn_location
    moves_taken = 0        

    while(world_still_dirty):
        moves_taken +=1
        if moves_taken == 10000:
            break
        dirty = world[location]
        if(not dirty):
            action = reflex_rules[location]['Clean']
        else: 
            action = reflex_rules[location]['Dirty']
        if(action == 'Suck'):
            world_still_dirty -= 1
            world[location] = 0
        else:
            location += move_dict[action]
            # if location == 3:
                # reflex_rules[3]['Clean'] = 'Down' if reflex_rules[3]['Clean'] == 'Up' else 'Up' 

    return moves_taken

def random_world(dirtcount, world):

    random_actions = ['Suck', 'Up', 'Right', 'Down', 'Left', 'Nothing']

    spawn_location = random.randint(0, 8)
    world_still_dirty = dirtcount
    location = spawn_location
    moves_taken = 0 
    while(world_still_dirty):
        moves_taken +=1
        dirty = world[location]
        action = random_actions[random.randint(0,5)] 
        if(dirty and action == 'Suck'):
            world_still_dirty -= 1
            world[location] = 0
        elif(action == 'Suck' or action == 'Nothing'):
            continue
        else:
            if can_move(location, action):
                location = (location + move_dict[action])
            else:
                continue 

    return moves_taken

def can_move(location, action):
    if(location == 4):
        return True
    elif(location in [6, 7, 8] and action == 'Up') or (location in [0, 1, 2] and action == 'Down'):
        return True
    elif(location in [3, 5] and action in ['Up', 'Down']):
        return True
    elif(location in [0, 3, 6, 1, 7] and action == 'Right') or (location in [2, 5, 8, 1, 7] and action == 'Left'):
        return True
    return False
    


def murphys_reflex_world(dirtcount,reflex_rules, world):

    spawn_location = random.randint(0, 8)
    murphs_dirt = 0
    murphs_dirt_sensor = 0
    world_still_dirty = dirtcount
    location = spawn_location
    moves_taken = 0        
    while(world_still_dirty):
        moves_taken +=1
        if moves_taken == 10000:
            break
        murphs_dirt_sensor +=1
        dirty = world[location] #actually dirt on space
        if murphs_dirt_sensor %10 == 0:
            dirty_error = (dirty+1)%2
        else: 
             dirty_error = 0
        if (not dirty and not dirty_error) or (dirty and dirty_error): #if it's not dirty and no error or if it's dirty but thinks its clean
                action = reflex_rules[location]['Clean']
        elif (dirty and not dirty_error) or (not dirty and dirty_error): 
            action = reflex_rules[location]['Dirty']
        if(action == 'Suck'):
            murphs_dirt+=1
            if dirty_error: #if it thinks there's dirt erroneously, just do nothing 
                if murphs_dirt %4==0:
                    world[location] = 1
                    world_still_dirty +=1 #deposit dirt
                else:
                    continue
            else:
                world_still_dirty -= 1
                world[location] = 0
        else:
            location += move_dict[action]
            # if location == 3:
            #     reflex_rules[3]['Clean'] = 'Down' if reflex_rules[3]['Clean'] == 'Up' else 'Up' 
    return moves_taken

def murphys_random_world(dirtcount, world):

    spawn_location = random.randint(0, 8)
    random_actions = ['Suck', 'Up', 'Right', 'Down', 'Left', 'Nothing']
    murphs_dirt = 0
    murphs_dirt_sensor = 0
    world_still_dirty = dirtcount
    location = spawn_location
    moves_taken = 0  
    while(world_still_dirty):
        moves_taken +=1
        murphs_dirt_sensor +=1
        dirty = world[location] #actually dirt on space
        if murphs_dirt_sensor %10 == 0:
            dirty_error = (dirty+1)%2
        else: 
             dirty_error = 0
        action = random_actions[random.randint(0,5)] 
        if(action == 'Suck'):
            murphs_dirt+=1
            if dirty_error: #if it thinks there's dirt erroneously, just do nothing 
                if murphs_dirt %4==0:
                    world[location] = 1 # deposit dirt
                    world_still_dirty+=1
                else:    
                    continue
            elif(dirty):
                world_still_dirty -= 1
                world[location] = 0
        elif(action == 'Nothing'):
            continue
        elif can_move(location, action):
            location = (location + move_dict[action])
        else: 
            continue

    return moves_taken

def reflex_agent():

    reflex_rules = {0:{'Dirty':'Suck', 'Clean':'Right'},
                    1:{'Dirty':'Suck', 'Clean':'Right'},
                    2:{'Dirty':'Suck', 'Clean':'Down'},
                    3:{'Dirty':'Suck', 'Clean':'Down'},
                    4:{'Dirty':'Suck', 'Clean':'Left'},
                    5:{'Dirty':'Suck', 'Clean':'Left'},
                    6:{'Dirty':'Suck', 'Clean':'Right'},
                    7:{'Dirty':'Suck', 'Clean':'Right'},
                    8:{'Dirty':'Suck', 'Clean':'Up'}
                } 
   
    num_trials = 1000
    avg1 = 0
    avg3 = 0
    avg5 = 0 
    for i in range(0, num_trials):
        world1, world3, world5 = generate_worlds()
        avg1+= reflex_world(1, reflex_rules, world1)
        avg3+= reflex_world(3, reflex_rules, world3)
        avg5+= reflex_world(5, reflex_rules, world5)
    print('Reflex Averages:\nWorld 1: {} \nWorld 3: {}\nWorld 5: {}'.format(avg1/num_trials, avg3/num_trials, avg5/num_trials))

def random_agent():
    
    num_trials = 1000
    avg1 = 0
    avg3 = 0
    avg5 = 0 
    print('Calculating Random Averages (takes a minute)')
    for i in range(0, num_trials):
        world1, world3, world5 = generate_worlds()
        avg1+= random_world(1, world1)
        avg3+= random_world(3, world3)
        avg5+= random_world(5, world5)
    print('Random Averages:\nWorld 1: {} \nWorld 3: {}\nWorld 5: {}'.format(avg1/num_trials, avg3/num_trials, avg5/num_trials))

def murphys_reflex_agent():

    reflex_rules = {0:{'Dirty':'Suck', 'Clean':'Right'},
                    1:{'Dirty':'Suck', 'Clean':'Right'},
                    2:{'Dirty':'Suck', 'Clean':'Down'},
                    3:{'Dirty':'Suck', 'Clean':'Down'},
                    4:{'Dirty':'Suck', 'Clean':'Left'},
                    5:{'Dirty':'Suck', 'Clean':'Left'},
                    6:{'Dirty':'Suck', 'Clean':'Right'},
                    7:{'Dirty':'Suck', 'Clean':'Right'},
                    8:{'Dirty':'Suck', 'Clean':'Up'}
                } 
   
    num_trials = 1000
    avg1 = 0
    avg3 = 0
    avg5 = 0 
    for i in range(0, num_trials):
        world1, world3, world5 = generate_worlds()
        avg1+= murphys_reflex_world(1,reflex_rules, world1)
        avg3+= murphys_reflex_world(3,reflex_rules, world3)
        avg5+= murphys_reflex_world(5,reflex_rules, world5)
    print('Murphy\'s Reflex Averages:\nWorld 1: {} \nWorld 3: {}\nWorld 5: {}'.format(avg1/num_trials, avg3/num_trials, avg5/num_trials))    

def murphys_random_agent():
    
    num_trials = 1000
    avg1 = 0
    avg3 = 0
    avg5 = 0 
    print('Calculating Murphys Random Averages (takes a minute)')
    for i in range(0, num_trials):
        world1, world3, world5 = generate_worlds()
        avg1+= random_world(1, world1)
        avg3+= random_world(3, world3)
        avg5+= random_world(5, world5)
    print('Murphys Random Averages:\nWorld 1: {} \nWorld 3: {}\nWorld 5: {}'.format(avg1/num_trials, avg3/num_trials, avg5/num_trials))


def main():
    
    reflex_agent()
    random_agent()
    murphys_reflex_agent()
    murphys_random_agent()

    return     

if __name__ == "__main__":
    main()