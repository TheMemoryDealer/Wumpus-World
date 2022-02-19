# game.py
#
# The top level loop that runs the game until Link wins or loses.
#
# run this using:
#
# python3 game.py
#
# Written by: Simon Parsons
# Last Modified: 25/08/20

from world import World
from link  import Link
from dungeon import Dungeon
import config
import utils
import time
from termcolor import colored

# How we set the game up. Create a world, then connect player and
# display to it.
gameWorld = World()
player = Link(gameWorld)
display = Dungeon(gameWorld)
time.sleep(5)
# Now run...
while not(gameWorld.isEnded()):
    gameWorld.updateLink(player.make_move())
    # print(player.flag)
    # print('My total loot - ', gameWorld.goods)
    gameWorld.updateWumpus()
    # Uncomment this for a printout of world state
    # utils.printGameState(gameWorld)
    display.update()
    time.sleep(4.7)

if gameWorld.status == utils.State.WON:
    if config.test == False:
        print(colored("You won!", 'yellow', attrs=['reverse']))
    else:
        print("You won!")
else:
    if config.test == False:
        print(colored("You lost!", 'red', attrs=['reverse']))
        print(gameWorld.reason.name)
    else:
        print("You lost!")
        print(gameWorld.reason.name)
