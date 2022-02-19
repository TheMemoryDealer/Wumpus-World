# Wumpus-World


Wumpus-World is a 2D game environment made to test AI agent functionality. The initial world is written by Prof. Simon Parsons (https://scholar.google.co.uk/citations?user=L9z6PakAAAAJ&hl=en), Q-learning functionality + minor bug fixes added 2021.

<p align="center">
  <div align="center">
  STATIC ENV
</div>
  <img src="https://github.com/TheMemoryDealer/Wumpus-World/blob/main/assets/expl1.gif" width="900" alt="animated" />
  <div align="center">
  DYNAMIC ENV
</div>
  <img src="https://github.com/TheMemoryDealer/Wumpus-World/blob/main/assets/expl4.gif" width="900" alt="animated" />
    <div align="center">
  DYNAMIC ENV, 2 WUMPUS
</div>
  <img src="https://github.com/TheMemoryDealer/Wumpus-World/blob/main/assets/expl6.gif" width="900" alt="animated" />
</p>

### Game updates:
* Minimap is generated and printed to console (reward map can be as well) IN CORRECT ROTATION!
* Functionality to check whether room is occupied.
* Colored print to console.
* Keep track of gold collected.
* Links expected route functionality (still taking non-deterministic actions into account so might not be accurate) and action to be taken next (UP,DOWN,LEFT,RIGHT).
* What I call 'suicide functionality'. If Link's next goal is closed off by pits or Wumpus', he realizes there is no way out and starts performing random actions.



Run the game using:
`python game.py`

If on Linux, run like so to produce log file:
`python batch.py | tee log.txt`

dungeon.py  -- draws the dungeon on the screen.

game.py     -- runs the game until Link wins or loses.

graphics.py -- simple Python graphics.

utils.py    -- utilities used in a few places.

world.py    -- keeps track of everything (used by Dungeon to draw).

batch.py    -- runs simulations.


### Simuation results:
Grid Size: 6x6-19x19

Enemy Count: 1-2

Pit Count: 1-19

Gold Count: 1-4

Environments: STATIC/DYNAMIC

Outcome: WON/LOST

Death Reason: PIT/WUMPUS

|   ENV   | OUTCOME | REASON |     |
|:-------:|:-------:|:------:|:---:|
| Dynamic |   Lost  |   Pit  | 10% |
| Dynamic |   Lost  | Wumpus | 66% |
| Dynamic |   Won   |    -   | 22% |
|  Static |   Lost  |   Pit  | 20% |
|  Static |   Lost  | Wumpus |  2% |
|  Static |   Won   |    -   | 78% |
