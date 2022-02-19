# world.py
#
# A file that represents the Wumpus World, keeping track of the
# position of all the objects: pits, Wumpus, gold, and the agent, and
# moving them when necessary.
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

import random
import config
import utils
from utils import State, Reason, Pose, Directions
from termcolor import colored

class World():

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.maxX = config.worldLength - 1
        self.maxY = config.worldBreadth - 1
        self.status = State.PLAY
        self.reason = None
        self.looted = False
        self.taken = []
        self.goods = 0
        
        self.wLoc = []
        # Wumpus
        if config.dynamic == True:
            # Wumpus can be chilling anywhere + checking for them somehow breaks tests
            # it doesnt matter where he/they spawn as they'll move anyways.
            # 
            for i in range(config.numberOfWumpus):
                wumpus = utils.pickRandomPose(self.maxX, self.maxY)
                self.wLoc.append(wumpus)
                self.taken.append(wumpus) # dont spawn anything on them though
        else:
            avail = True
            for i in range(config.numberOfWumpus):
                while True:
                    test = utils.pickRandomPose(self.maxX, self.maxY)  
                    avail = True
                    for pose in self.taken:
                        if pose.x == test.x and pose.y == test.y: 
                            avail = False

                    if avail == True:
                        self.wLoc.append(test)
                        self.taken.append(test)
                        break

        # Gold
        self.gLoc = [] # Occupation checking was written by Stuart Jessup https://github.com/Bluboy456
        avail = True
        for i in range(config.numberOfGold):
            while True:
                test = utils.pickRandomPose(self.maxX, self.maxY)  
                avail = True
                for pose in self.taken:
                    if pose.x == test.x and pose.y == test.y: 
                        avail = False

                if avail == True:
                    self.gLoc.append(test)
                    self.taken.append(test)
                    break

        # Pits
        self.pLoc = []
        for i in range(config.numberOfPits):
            while True:
                test = utils.pickRandomPose(self.maxX, self.maxY) 
                avail = True 
                for pose in self.taken:
                    if pose.x == test.x and pose.y == test.y:
                        avail = False

                if avail == True:
                    self.pLoc.append(test)
                    self.taken.append(test)
                    break

         # Link
        self.lLoc = []
        while True:
            test = utils.pickRandomPose(self.maxX, self.maxY)
            avail = True 
            for pose in self.taken:
                if pose.x == test.x and pose.y == test.y: 
                    avail = False

            if avail == True:
                self.lLoc = test
                self.taken.append(test)
                break
        
    #
    # Access Methods
    #
    # These are the functions that should be used by Link to access
    # information about the world.

    #What is the breadth of the world?
    def getMaxX(self):
        return self.maxX

    def getMaxY(self):
        return self.maxY

    # Where is/are the Wumpus?
    def getWumpusLocation(self):
        return self.wLoc

    # Where is Link?
    def getLinkLocation(self):
        return self.lLoc

    # Where is the Gold?
    def getGoldLocation(self):
        return self.gLoc

    # Where are the Pits?
    def getPitsLocation(self):
        return self.pLoc

    # Did we just loot some gold?
    def justLooted(self):
        return self.looted

    # What is the current game state?
    def getGameState(self):
        return self.status

    # Does Link feel the wind?
    def linkWindy(self):
        return isWindy(lLoc)

    # Does Link smell the Wumpus?
    def linkSmelly(self):
        return isSmelly(lLoc)

    # Does Link see the glitter?
    def linkGlitter(self):
        return isGlitter(lLoc)
 
    #
    # Methods
    #
    # These are the functions that are used to update and report on
    # world information.

    def isEnded(self):
        dead = False
        won = False
        # Has Link met the Wumpus?
        for i in range(len(self.wLoc)):
            if utils.sameLocation(self.lLoc, self.wLoc[i]):
                if config.test == False:
                    print(colored("Oops! Met the Wumpus", 'blue', attrs=['reverse']))
                else:
                    print("Oops! Met the Wumpus")
                dead = True
                self.status = State.LOST
                self.reason = Reason.WUMPUS
                
        # Did Link fall in a Pit?
        for i in range(len(self.pLoc)):
            if utils.sameLocation(self.lLoc, self.pLoc[i]):
                if config.test == False:
                    print(colored("Arghhhhh! Fell in a pit", 'blue', attrs=['reverse']))
                else:
                    print("Arghhhhh! Fell in a pit")
                dead = True
                self.status = State.LOST
                self.reason = Reason.PIT
                

        # Did Link loot all the gold?
        if len(self.gLoc) == 0:
            won = True
            self.status = State.WON
            
        if dead == True or won == True:
            if config.test == False:
                print(colored("Game Over!", 'magenta', attrs=['reverse']))
            else:
                print("Game Over!")
            return True
            
    # Implements the move chosen by Link
    def updateLink(self, direction):
        # Set the looted flag to False
        self.looted = False
        # Implement non-determinism if appropriate
        direction = self.probabilisticMotion(direction)
        if direction == Directions.NORTH:
            if self.lLoc.y < self.maxY:
                self.lLoc.y = self.lLoc.y + 1
            
        if direction == Directions.SOUTH:
            if self.lLoc.y > 0:
                self.lLoc.y = self.lLoc.y - 1
                
        if direction == Directions.EAST:
            if self.lLoc.x < self.maxX:
                self.lLoc.x = self.lLoc.x + 1
                
        if direction == Directions.WEST:
            if self.lLoc.x > 0:
                self.lLoc.x = self.lLoc.x - 1

        # Did Link just loot some gold?
        match = False
        index = 0
        for i in range(len(self.gLoc)):
            if utils.sameLocation(self.lLoc, self.gLoc[i]):
                match = True
                index = i
                self.looted = True
                if config.test == False:
                    print(colored("Gold looted!", 'yellow'))
                else:
                    print("Gold looted!")
                self.goods += 1
                print('My total loot - ', self.goods)

        # Assumes that golds have different locations. Or, that only
        # one gold can be picked up in a given turn.
        if match:
            self.gLoc.pop(index)

    # Implement nondeterministic motion, if appropriate.
    def probabilisticMotion(self, direction):
        if config.nonDeterministic:
            dice = random.random()
            if dice < config.directionProbability:
                return direction
            else:
                return self.sideMove(direction)
        else:
            return direction
        
    # Move at 90 degrees to the original direction.
    def sideMove(self, direction):
        # Do we head left or right of the intended direction?
        dice =  random.random()
        if dice > 0.5:
            left = True
        else:
            left = False
        if direction == Directions.NORTH:
            if left:
                return Directions.WEST
            else:
                return Directions.EAST

        if direction == Directions.SOUTH:
            if left:
                return Directions.EAST
            else:
                return Directions.WEST

        if direction == Directions.WEST:
            if left:
                return Directions.SOUTH
            else:
                return Directions.NORTH

        if direction == Directions.EAST:
            if left:
                return Directions.NORTH
            else:
                return Directions.SOUTH
            
    # Move the Wumpus if that is appropriate
    #
    # TODO - stop Wumpus moving over pits
    #
    def updateWumpus(self):
        if config.dynamic:
            # Head towards Link
            target = self.lLoc
            for i in range(len(self.wLoc)):
                # If same x-coordinate, move in the y direction
                if self.wLoc[i].x == target.x:
                    self.wLoc[i].y = self.reduceDifference(self.wLoc[i].y, target.y)        
                # If same y-coordinate, move in the x direction
                elif self.wLoc[i].y == target.y:
                    self.wLoc[i].x = self.reduceDifference(self.wLoc[i].x, target.x)        
                # If x and y both differ, approximate a diagonal
                # approach by randomising between moving in the x and
                # y direction.
                else:
                    dice = random.random()
                    if dice > 0.5:
                        self.wLoc[i].y = self.reduceDifference(self.wLoc[i].y, target.y)        
                    else:
                        self.wLoc[i].x = self.reduceDifference(self.wLoc[i].x, target.x)        

    # Move value towards target.
    def reduceDifference(self, value, target):
        if value < target:
            return value+1
        elif value > target:
            return value-1
        else:
            return value

    # Is the given location smelly?
    #
    # A location is smelly if it is next to the Wumpus
    def isSmelly(self, location):
        if isAjacent(self.Wloc, location):
            return True
        else:
            return False

    # Is the given location windy? 
    def isWindy(self, location):
        if isAjacent(self.ploc, location):
            return True
        else:
            return False

     # Does the given location glitter? 
    def isGlitter(self, location):
        if isAjacent(self.gloc, location):
            return True
        else:
            return False
        
    # Is the location loc next to any of the locations in locList.
    #
    # To be adjacent in this sense, you either have to be at the same
    # x coordinate and have a y coordinate that differs by 1, or in
    # the same y coordinate and have an x coordinate that differs by
    # one.
    def isAjacent(locList, loc):
        for aloc in locList:
            # Ajacency holds if it holds for any location in locList.
            if aloc.x == loc.x:
                if aloc.y == loc.y + 1 or aloc.y == loc.y - 1:
                    return True
                else:
                    return False
            elif aloc.y == loc.y:
                if aloc.x == loc.x + 1 or aloc.x == loc.x - 1:
                    return True
                else:
                    return False
            else:
                return False
            
            
