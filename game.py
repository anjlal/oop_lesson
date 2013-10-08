import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7
WIN_SPACE = None
NUM_ELTS = 10
NUM_ITEMS = 4
LEVEL_COUNTER = 1
FINAL_LEVEL = 5
GAME_STATE = "win"

#### Put class definitions here ####
class Character(GameElement):
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
    IMAGE = "Cat"
    current_dir = None

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class Stark(Character):
    IMAGE = "Stark"

class Baratheon(Character):
    IMAGE = "Baratheon"

class Lannister(Character):
    IMAGE = "Lannister"

class Targaryen(Character):
    IMAGE = "Targaryen"

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Block(GameElement):
    IMAGE = "Block"
    SOLID = False

    def interact(self, player):
        # do stuff like move over
        direction = player.current_dir
        next_x, next_y = self.next_pos(direction)

        if not in_bounds(next_x, next_y) or existing_element(next_x, next_y) or (next_x, next_y) == WIN_SPACE:
            self.SOLID = True
        elif direction:
            move(direction, self)
            self.SOLID = False

        # check if next move will result in covering win space, if so, player loses

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

class IronThrone(GameElement):
    SOLID = True
    IMAGE = "Iron Throne"

    def interact(self, player):
        global GAME_STATE
        GAME_STATE = "lost"
        GAME_BOARD.draw_msg("You ascend the Iron Throne. You are now the true ruler of Westeros! Press SPACE to restart.")
    # disable movement somehow, or give you option to reset?

class Collectable(GameElement):
    SOLID = False
    NAME = "item"

    def interact(self, player):
        player.inventory.append(self)

        GAME_BOARD.draw_msg("You just acquired a %s! You have %d items!" % (self.NAME, len(player.inventory)))

    def __str__(self):
        return self.NAME

class RedGem(Collectable):

    IMAGE = "RedGem"
    NAME = "Gem"


class GrayGem(Collectable):

    IMAGE = "GrayGem"
    NAME = "Gem"

class YellowGem(Collectable):

    IMAGE = "YellowGem"
    NAME = "Gem"

class BlackGem(Collectable):

    IMAGE = "BlackGem"
    NAME = "Gem"

class Crown(Collectable):

    IMAGE = "Crown"
    NAME = "Crown"

class WhiteWalker(GameElement):
    IMAGE = "White Walker"
    SOLID = True

    def interact(self, player):
        global GAME_STATE
        GAME_STATE = "lost"
        GAME_BOARD.draw_msg("You lost the game. Press SPACE to restart.")

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class TallWall(GameElement):
    IMAGE = "Tall Wall"
    SOLID = True

class Tree(GameElement):
    IMAGE = "ShortTree"
    SOLID = True

class Goblet(GameElement):
    IMAGE = "Goblet"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

class Dragon(GameElement):
    IMAGE = "Dragon"
    SOLID = True

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        #go to the final level
        global PLAYER

        clear_board()
        GAME_BOARD.create("StoneBlock","Block")
        throne = IronThrone()
        place_on_board(throne, 3, 2)
        place_on_board(PLAYER, 3, 6)

####   End class definitions    ####

def existing_element(x, y):
    existing_el = GAME_BOARD.get_el(x, y)
    return existing_el

def move(direction, obj):
    next_location = obj.next_pos(direction)
    obj.current_dir = direction
    next_x = next_location[0]
    next_y = next_location[1]

    if in_bounds(next_x,next_y):
        existing_el = existing_element(next_x, next_y)

        if existing_el:
            existing_el.interact(obj)

        if existing_el is None or not existing_el.SOLID:
            # If there's nothing there _or_ if the existing element is not solid, walk through
            GAME_BOARD.del_el(obj.x, obj.y)
            GAME_BOARD.set_el(next_x, next_y, obj)

def in_bounds(x, y):
    if x in range(0,GAME_WIDTH) and y in range(0,GAME_HEIGHT):
        return True
    else:
        return False

def place_on_board(obj, x, y):
    GAME_BOARD.register(obj)
    GAME_BOARD.set_el(x, y, obj)

def clear_board():
    for x in range(0,GAME_WIDTH):
        for y in range(0,GAME_HEIGHT):
            GAME_BOARD.del_el(x, y)
    
    GAME_BOARD.erase_msg()

def initialize():
    """Put game initialization code here"""
    global PLAYER # this means we use the global var PLAYER and cannot have a local var named PLAYER
    
    coordinates = generate_coords()

    PLAYER = Stark()
    tree = Tree()
    ww = WhiteWalker()
    crown = Crown()
    gray_gem = GrayGem()

    GAME_BOARD.create("Snow","Snow")
    GAME_BOARD.draw_msg("Level " + str(LEVEL_COUNTER) + ". Winter is coming.")
    generate_level(coordinates, [PLAYER, ww, gray_gem, crown, tree, tree, gray_gem, tree, tree, gray_gem, tree])

    # for i in range(0,NUM_ELTS):
    #     place_on_board(elts[i], coordinates[i][0], coordinates[i][1])

def generate_level(coords, list_of_elts):
    for i in range(0,NUM_ELTS):
        place_on_board(list_of_elts[i], coords[i][0], coords[i][1])

def generate_coords():
    coords = []
    
    while len(coords) < NUM_ELTS + 1:
        tup = ( random.randrange(0, GAME_WIDTH), random.randrange(0, GAME_HEIGHT) )
        if tup not in coords:
            coords.append(tup)

    global WIN_SPACE
    WIN_SPACE = coords.pop()
    print WIN_SPACE

    return coords

def keyboard_handler():
    # all of your keyboard event listening has to happen here, but you can add different game states if you want...
    global PLAYER
    global WIN_SPACE
    global LEVEL_COUNTER
    global GAME_STATE

    crown = Crown()
    tree = Tree()
    rock = Rock()

    if GAME_STATE == "win":

        direction = None

        if KEYBOARD[key.UP]:
            direction = "up"
        elif KEYBOARD[key.DOWN]:
            direction = "down"
        elif KEYBOARD[key.LEFT]:
            direction = "left"
        elif KEYBOARD[key.RIGHT]:
            direction ="right"

        if direction:
            move(direction, PLAYER)
            if (PLAYER.x, PLAYER.y) == WIN_SPACE:
                if len(PLAYER.inventory) == NUM_ITEMS:
                    LEVEL_COUNTER += 1
                    clear_board()
                    coords = generate_coords()

                    if LEVEL_COUNTER == 2:
                        # baratheon
                        PLAYER = Baratheon()
                        GAME_BOARD.create("StoneBlock","GrassBlock")
                        GAME_BOARD.draw_msg("Level " + str(LEVEL_COUNTER) + ". Ours is the fury.")

                        goblet = Goblet()
                        y_gem = YellowGem()

                        generate_level(coords, [PLAYER, goblet, y_gem, crown, tree, tree, y_gem, tree, tree, y_gem, tree])
                    elif LEVEL_COUNTER == 3:
                        #lannister
                        PLAYER = Lannister()
                        GAME_BOARD.create("StoneBlock","Dirt")
                        GAME_BOARD.draw_msg("Level " + str(LEVEL_COUNTER) + ". A Lannister always pays his debts.")

                        chest = Chest()
                        red_gem = RedGem()

                        generate_level(coords, [PLAYER, chest, red_gem, crown, tree, tree, red_gem, tree, tree, red_gem, tree])
                    elif LEVEL_COUNTER == 4:
                        #targaryen
                        PLAYER = Targaryen()
                        GAME_BOARD.create("Block","StoneBlock")
                        GAME_BOARD.draw_msg("Level " + str(LEVEL_COUNTER) + ". Fire and blood!")

                        dragon = Dragon()
                        black_gem = BlackGem()

                        generate_level(coords, [PLAYER, dragon, black_gem, crown, tree, tree, black_gem, tree, tree, black_gem, tree])
                    
                    elif LEVEL_COUNTER == FINAL_LEVEL:
                        # draw castle
                        GAME_BOARD.create("StoneBlock","GrassBlock")
                        GAME_BOARD.draw_msg("Claim what is yours!")

                        WIN_SPACE = None
                        wall = Wall()
                        tall_wall = TallWall()
                        door = Door()

                        place_on_board(PLAYER, 3, 6)
                        place_on_board(wall, 1, 2)
                        place_on_board(tall_wall, 2, 2)
                        place_on_board(door, 3, 2)
                        place_on_board(tall_wall, 4, 2)
                        place_on_board(wall, 5, 2)

        if KEYBOARD[key.I]:
            inv = "Inventory: "
            for item in PLAYER.inventory:
                inv += str(item) + " "
            GAME_BOARD.draw_msg(inv)

        if KEYBOARD[key.C]:
            if LEVEL_COUNTER != FINAL_LEVEL:
                clear_board()
                coords = generate_coords()
                PLAYER = Character() # this makes a new player instance so will also get rid of your inventory. change this if you want to keep items.
                generate_level(coords, [PLAYER, gem, rock, rock2, block, gem2, rock3, rock4])

    elif GAME_STATE == "lost":
        if KEYBOARD[key.SPACE]:
            GAME_STATE = "win"
            GAME_BOARD.erase_msg()
            clear_board()
            initialize()