# link.py
#
# The code that defines the behaviour of Link. You should be able to
# do all you need in here, using access methods from world.py, and
# using make_move() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import world
import random
import utils
from utils import Directions
import config
import numpy as np
import time
from termcolor import colored


class Link():

    def __init__(self, dungeon):

        # Make a copy of the world an attribute, so that Link can query the state of the world
        self.gameWorld = dungeon
        self.minimap = [] # to see
        self.rewards = [] # to hold values (int)
        self.q_values = np.zeros((config.worldLength, config.worldBreadth, 4))
        self.agentLoc = self.gameWorld.getLinkLocation()
        # get map dims
        self.minimapX = config.worldLength-1
        self.minimapY = config.worldBreadth-1 # -1 because 0 indexing
        # What moves/actions are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        self.globalActionStorage = []
        self.flag = False
        self.enemylocs = []
        
    '''Func to print minimap to console '''
    def print_minimap_properly(self):
        print('MAP IS:')
        print(np.rot90(np.flipud(self.minimap),3)) # rotate 270 degrees and flip upside down to see as it is in game
        
    def build_map(self): # builds minimap for print to console then duplicates to statemap for computation
        # print(self.minimapX)
        # print(self.minimapY)
        self.minimap = np.zeros((config.worldLength, config.worldBreadth), dtype = str)
        # self.minimap.fill('s')
        # for Wumpus
        w = self.gameWorld.getWumpusLocation() # this is list so loop
        # print(type(w))
        for i in w:
            self.minimap[i.x, i.y] = "W" 
        # for Pit
        p = self.gameWorld.getPitsLocation() # this is list so loop
        # print(type(p))
        for i in p:
            self.minimap[i.x, i.y] = "P"
        # for Gold
        g = self.gameWorld.getGoldLocation() # this is list so loop
        # print(type(g))
        for i in g:
            self.minimap[i.x, i.y] = "G"
        # for Link
        self.minimap[self.agentLoc.x, self.agentLoc.y] = "L"

        self.rewards = np.zeros((config.worldLength, config.worldBreadth), dtype = int) # reconvert minimap to int type
        if config.dynamic == True:
            # now replace with state values
            for ix,iy in np.ndindex(self.minimap.shape):
                if self.minimap[ix,iy] == 'P':
                    self.rewards[ix,iy] = -100
                elif self.minimap[ix,iy] == 'W': 
                    self.rewards[ix,iy] = -100
                    self.enemylocs.append([ix, iy])
                    for loc in self.enemylocs:
                        # chech if not on end or start of map
                        if loc[0] < self.minimapX:
                            if self.minimap[loc[0]+1,loc[1]] != 'P' or self.minimap[loc[0]+1,loc[1]] != 'G': # if not gold or pit
                                self.rewards[loc[0]+1,loc[1]] = -50
                        if loc[0] != 0:
                            if self.minimap[loc[0]-1,loc[1]] != 'P' or self.minimap[loc[0]-1,loc[1]] != 'G': # if not gold or pit
                                self.rewards[loc[0]-1,loc[1]] = -50
                        if loc[1] < self.minimapY:
                            if self.minimap[loc[0],loc[1]+1] != 'P' or self.minimap[loc[0],loc[1]+1] != 'G': # if not gold or pit
                                self.rewards[loc[0],loc[1]+1] = -50
                        if loc[1] != 0:
                            if self.minimap[loc[0],loc[1]-1] != 'P' or self.minimap[loc[0],loc[1]-1] != 'G': # if not gold or pit
                                self.rewards[loc[0],loc[1]-1] = -50
                elif self.minimap[ix,iy] == 'G':
                    self.rewards[ix,iy] = 10
                # else:
                #     self.rewards[ix,iy] = -1
            self.rewards[self.rewards == 0] = -1 
        else:
            # now replace with state values
            for ix,iy in np.ndindex(self.minimap.shape):
                if (self.minimap[ix,iy] == 'P' or self.minimap[ix,iy] == 'W'): 
                    self.rewards[ix,iy] = -100
                elif (self.minimap[ix,iy] == 'G'):
                    self.rewards[ix,iy] = 100
                else:
                    self.rewards[ix,iy] = -1
        # print(self.minimap)
        self.enemylocs = [] # enemy locs will have changed so reset
        

    #define a function that determines if the specified location is a terminal state
    def is_terminal_state(self, current_y, current_x):
        if self.rewards[current_y, current_x] == -1 or self.rewards[current_y, current_x] == -50: # Link can be next to Wumpus
            return False
        else:
            return True
        
    #define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
    def get_next_action(self, current_y, current_x, epsilon):
        #if a randomly chosen value between 0 and 1 is less than epsilon, 
        #then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_y, current_x])
        else: #choose a random action
            return np.random.randint(4)
        
    #define a function that will get the next location based on the chosen action
    def get_next_location(self, current_y, current_x, action_index):
        new_x = current_y
        new_y = current_x
        if self.moves[action_index] == Directions.NORTH and current_y > 0:
            new_x -= 1
        elif self.moves[action_index] == Directions.EAST and current_x < self.minimapX:
            new_y += 1
        elif self.moves[action_index] == Directions.SOUTH and current_y < self.minimapY:
            new_x += 1
        elif self.moves[action_index] == Directions.WEST and current_x > 0:
            new_y -= 1
        return new_x, new_y
    
    #Define a function that will get the shortest path
    def get_shortest_path(self, start_y, start_x):
        #return immediately if no way to next goal
        if self.flag == True:
            return []
        current_y, current_x = start_y, start_x
        shortest_path = []
        shortest_path.append([current_y, current_x])
        #continue moving along the path until we reach the goal
        while not self.is_terminal_state(current_y, current_x):
            #get the best action to take
            action_index = self.get_next_action(current_y, current_x, config.directionProbability)
            # add all actions to global array
            self.globalActionStorage.append(action_index) # hack to get the needed actions out easily
            #move to the next location on the path, and add the new location to the list
            current_y, current_x = self.get_next_location(current_y, current_x, action_index)
            shortest_path.append([current_y, current_x])
        shortest_path.pop(0) # we already know where we are
        
        # if len(shortest_path) > 50: # Something went wrong, disregard to save ram
        #     return []
        
        return shortest_path
        
    def make_move(self):
        
        # utils.printGameState(self.gameWorld)
        # print(self.moves)
        # print(world.World.getGameState(self.gameWorld))
        
        self.build_map()
        
        #define training parameters
        epsilon = config.directionProbability #the percentage of time when we should take the best action (instead of a random action)
        discount_factor = 0.75 #discount factor for future rewards
        learning_rate = 0.9 #the rate at which the AI agent should learn

        for episode in range(1000):
            #get the starting location for this episode
            y, x = self.agentLoc.x, self.agentLoc.y # these are actually swapped (x,y)->(y,x) so re-swap in assignment

            # move until gold, wumpus or pit reached
            while not self.is_terminal_state(y, x):
                #choose which action to take (i.e., where to move next)
                action_index = self.get_next_action(y, x, epsilon)

                #perform the chosen action, and transition to the next state
                old_y, old_x = y, x #store the old row and column indexes
                y, x = self.get_next_location(y, x, action_index)
                
                #receive the reward for moving to the new state, and calculate the temporal difference
                reward = self.rewards[y, x]
                old_q_value = self.q_values[y, old_x, action_index]
                
                ''' Yet another workaround. If Link is stuck with no way to gold and only a certain number of rooms to sucessfully traverse,
                return a random move regardless of the outcome. Would freeze the program without it and not continue tests. Not ideal as might 
                get scared and kill himself if 2 or more Wumpus' suround to him. '''
                
                # print('GAZEBOOOOOOOOOOOO', old_q_value)
                if (old_q_value == -3.999999999999999):
                    print('Might as well kill myself')
                    self.flag = True
                    return random.choice(list(self.moves))
                
                temporal_difference = reward + (discount_factor * np.max(self.q_values[y, x])) - old_q_value

                #update the Q-value for the previous state and action pair
                new_q_value = old_q_value + (learning_rate * temporal_difference)
                self.q_values[old_y, old_x, action_index] = new_q_value

        # print('Training complete!')
        
        #display shortest path
        route = self.get_shortest_path(self.agentLoc.x, self.agentLoc.y)
        # print('PATH IS - ', path)
        if config.test == False:
            print(colored('ROUTE IS - ', 'green'), colored(route, 'green', attrs=['reverse']))
        else:
            print('ROUTE IS - ', route)
            
        if config.test == True: # only print to log
            self.print_minimap_properly() 
        # print(np.rot90(np.flipud(self.rewards),3))
        # print(self.rewards)
        # time.sleep(5000000)
        # print(self.q_values)
        for i in self.globalActionStorage: # delete as will compute new ones each turn
            if i == 3:
                self.globalActionStorage = []
                
                ''' 2 types of print because its nice to have colored print to console but for testing im using Linux tee to output logs to file.
                Colorama makes it look super ugly hence the 2 types of print'''
                
                if config.test == False:
                    print(colored('I WILL NOW EXECUTE ACTION ', 'red'), i, colored('TO GO ', 'red'), colored('UP', 'red', attrs=['reverse', 'bold'])) # Up and down is inverted, this is a workaround
                else:
                    print('I WILL NOW EXECUTE ACTION ', i, ' TO GO ', 'UP')
                return Directions.SOUTH 
            elif i == 2:
                self.globalActionStorage = []
                if config.test == False:
                    print(colored('I WILL NOW EXECUTE ACTION ', 'red'), i, colored('TO GO ', 'red'), colored('DOWN', 'red', attrs=['reverse', 'bold']))
                else:
                    print('I WILL NOW EXECUTE ACTION ', i, ' TO GO ', 'DOWN')
                return Directions.NORTH 
            elif i == 1:
                self.globalActionStorage = []
                if config.test == False:
                    print(colored('I WILL NOW EXECUTE ACTION ', 'red'), i, colored('TO GO ', 'red'), colored('RIGHT', 'red', attrs=['reverse', 'bold']))
                else:
                    print('I WILL NOW EXECUTE ACTION ', i, ' TO GO ', 'RIGHT')
                return Directions.EAST
            elif i == 0:
                self.globalActionStorage = []
                if config.test == False:
                    print(colored('I WILL NOW EXECUTE ACTION ', 'red'), i, colored('TO GO ', 'red'), colored('LEFT', 'red', attrs=['reverse', 'bold']))
                else:
                    print('I WILL NOW EXECUTE ACTION ', i, ' TO GO ','LEFT')
                return Directions.WEST
            
