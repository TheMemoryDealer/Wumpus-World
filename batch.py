from world import World
from link  import Link
from dungeon import Dungeon
import utils
import time
from termcolor import colored
import config
import pandas as pd

# https://stackoverflow.com/a/48405769  this is amazing. I LOVE LINUX

config.numberOfGold = 1
config.numberOfPits = 10
config.numberOfWumpus = 1
config.worldLength = 4
config.test = True

df = pd.DataFrame(columns=['RUN', 'GRID', 'NWUMPUS', 'NPITS', 'NGOLD', 'ENV', 'OUTCOME', 'REASON', 'SUICIDEFLAG']) # create frame to store stats of game runs

counter = 1

for i in [False, True]: # for env
    for j in list(range(1, 5)): # for gold
        for k in list(range(1, 20)): # for pits
            ''' More than 2 Wumpus is just overkill, Link will most likely die'''
            for l in list(range(1,2)): # for wumpus
                for m in range(3): # 3 samples for each param spec
                    for n in list(range(6, 20)): # for grid size. Assume map is always square
                        print(' ') # to make log more readable
                        print('RUN - ', counter) # for log
                        config.numberOfGold = j
                        config.numberOfPits = k
                        config.numberOfWumpus = l
                        config.dynamic = i
                        config.worldBreadth = n
                        config.worldLength = n
                        #check if game dynamic or static
                        if config.dynamic == True:
                            env = 'Dynamic'
                        else:
                            env = 'Static'
                        # How we set the game up. Create a world, then connect player and
                        # display to it.
                        gameWorld = World()
                        player = Link(gameWorld)
                        # display = Dungeon(gameWorld)
                        # Now run...
                        while not(gameWorld.isEnded()):
                            gameWorld.updateLink(player.make_move())
                            gameWorld.updateWumpus()
                            # Uncomment this for a printout of world state
                            # utils.printGameState(gameWorld)
                            # display.update()
                            # time.sleep(0.3)

                        if gameWorld.status == utils.State.WON:
                            df.loc[counter] = counter, str(config.worldLength)+'x'+str(config.worldBreadth),config.numberOfWumpus,config.numberOfPits,config.numberOfGold,env, gameWorld.status.name,'-',player.flag
                        else:
                            df.loc[counter] = counter, str(config.worldLength)+'x'+str(config.worldBreadth),config.numberOfWumpus,config.numberOfPits,config.numberOfGold,env, gameWorld.status.name, gameWorld.reason.name,player.flag
                        counter+=1

''' Uncomment bellow 2 lines to print to console. Pretty useless as will most definitely trim the massive output.
Later found out you can do this https://stackoverflow.com/a/42407681 '''
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(df)
df.to_csv('stats.csv', encoding='utf-8', index=False)