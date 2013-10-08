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

GAME_WIDTH = 4
GAME_HEIGHT = 4
WIN_SPACE = None
NUM_ELTS = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

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

class NPC(Character):
    IMAGE = "Boy"
    SOLID = True

    def interact(self, player):
        GAME_BOARD.draw_msg("\"Hey! Give me your gem!\" Give him your gem? (Press Enter)")

        if KEYBOARD[key.E]:
            print "you pressed enter"
            #remove gem from inventory
            #delete boy from board
            #player.inventory.remove()

class Block(GameElement):
    IMAGE = "Block"
    SOLID = False

    def interact(self, player):
        # do stuff like move over
        direction = player.current_dir
        next_x, next_y = self.next_pos(direction)

        if not in_bounds(next_x, next_y) or existing_element(next_x, next_y):
            self.SOLID = True
        elif direction:
            move(direction, self)
            self.SOLID = False

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

class Gem(GameElement):

    def interact(self, player):
        if player.inventory.get(self.NAME, None) == None:
            player.inventory[self.NAME] = [self]
        else:
            player.inventory[self.NAME].append(self)
        print player.inventory

        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory[self.NAME])))

    IMAGE = "BlueGem"
    NAME = "Blue Gem"
    SOLID = False

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

    GAME_BOARD.draw_msg("We are making a game.")

    global PLAYER # this means we use the global var PLAYER and cannot have a local var named PLAYER
    
    coordinates = generate_coords()

    PLAYER = Character()
    gem = Gem()
    block = Block()
    gem2 = Gem()
    rock = Rock()
    rock2 = Rock()
    rock3 = Rock()
    rock4 = Rock()

    generate_level(coordinates, [PLAYER, gem, rock, rock2, block, gem2, rock3, rock4])

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

    return coords

def keyboard_handler():
    # all of your keyboard event listening has to happen here, but you can add different game states if you want...

    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction ="right"

    global PLAYER

    if direction:
        move(direction, PLAYER)
        if (PLAYER.x, PLAYER.y) == WIN_SPACE:
            gems = PLAYER.inventory.get("Blue Gem")
            if gems and len(gems) == 2:
                GAME_BOARD.draw_msg("You win!")
                clear_board()
                
                PLAYER = Character() # this makes a new player instance so will also get rid of your inventory. change this if you want to keep items.
                gem = Gem()
                block = Block()
                gem2 = Gem()
                rock = Rock()
                rock2 = Rock()
                rock3 = Rock()
                rock4 = Rock()

                coords = generate_coords()
                generate_level(coords, [PLAYER, gem, rock, rock2, block, gem2, rock3, rock4])

    if KEYBOARD[key.I]:
        inv = "Inventory: "
        for k, val in PLAYER.inventory.items():
            inv += str(len(val)) + " "
            inv += k
            if len(val) > 1:
                inv += "s" 

        GAME_BOARD.draw_msg(inv)

    if KEYBOARD[key.C]:
        clear_board()
        generate_coords()