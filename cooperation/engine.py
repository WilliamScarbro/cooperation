import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from pygame.time import Clock
from characters import *
import random
import events

class game:
    def __init__(self):
        self.height=800
        self.width=800
        self.fps=15
        self.clock=Clock()
        self.setup()
        self.game_loop()

    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.manager = main_manager()
    
    def handle_keys(self,keys):
        self.manager.handle_key(keys)

    def update(self):
        self.screen.fill((39,150,45))
        self.manager.render(self.screen)
        pygame.display.flip()

    def game_loop(self):
        running = True
        self.update()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running=False
                if event.type == KEYDOWN:
                    self.fps=15
                    pressed_keys = pygame.key.get_pressed()
                    self.handle_keys(pressed_keys)
                    self.update()
                if event.type == events.CHANGE_BOARD:
                    print("change_board")
                    event.data["board"].enter(event.data["person"])
                    self.manager.add_child(event.data["board"])
                    self.update()
                if event.type == events.NEW_MENU:
                    print("new menu")
            self.clock.tick(self.fps)
            if self.fps>5:
                self.fps-=.5

class manager(ABC):
    def __init__(self,child):
         self.child=child

    def return_control(self, data):
        self.child=None
        self.collect=data

    def handle_key(self, keys):
        if self.child!=None:
            self.child.handle_key(keys)
        else:
            self.real_handle_key(keys)
    def render(self, screen):
        if self.child!=None:
            self.child.render(screen)
        else:
            self.real_render(screen)
    
    def add_child(self, child):
        if self.child==None:
            self.child=child
        else:
            self.child.add_child(child)

class main_manager(manager):
    def __init__(self):
        super().__init__(board.from_file("board1.b"))
        self.child.players.gen_players()
        #self.child.initialize()
    
        
    
class menu(manager):
    def __init__(self, options, parent):
        super().__init__(None)
        self.options = options
        self.selection=0
        self.parent=parent

    def real_handle_key(self, keys):
        if keys[KEY_UP] and self.selection<len(self.options)-1:
            self.selection+=1
        if keys[KEY_DOWN] and self.selection>0:
            self.selection-=1
        if keys[ENTER]:
            self.parent.return_control(self.selection)

class board(manager):
    def __init__(self, width, height):
        super().__init__(None)
        self.width=width
        self.size=100
        self.height=height
        self.view_height=min(height,8)
        self.view_width=min(width,8)
        self.top_left=(0,0)
        self.landscape = layer(self)
        self.players = layer(self)
        self.background = layer(self)
        self.background.gen_background()
    
    def enter(person, pos):
        person.pos=entrance
        self.players.add_character(person)

    def exit(person):
        self.players.remove_character(person)

    @staticmethod
    def from_file(f_name):
        f = open("./boards/"+f_name)
        text = f.read().split()
        dim1 = int(text[0])
        dim2 = int(text[1])
        e_x = int(text[2])
        e_y = int(text[3])
        b = board(dim1, dim2)
        b.entrance = (e_x,e_y)
        text = text[4:]
        la = [[text[i] for i in range(j,j+dim1)] for j in range(0,dim1*dim2,dim1)]
        print(la)
        b.landscape.gen_from_arr(la)
        return b
 
    def initialize(self):
        self.size=100
        self.top_left=(0,0)
        self.landscape = layer(self)
        self.landscape.gen_landscape()
        self.players = layer(self)
        self.players.gen_players()
                
    def real_handle_key(self, keys):
        direc=None
        if keys[K_UP]:
            direc=(0,-1)
        if keys[K_DOWN]:
            direc=(0,1)
        if keys[K_RIGHT]:
            direc=(1,0)
        if keys[K_LEFT]:
            direc=(-1,0)
        if direc!=None:
            if self.test_move(direc):
                self.players.move_character("player",direc)
  
    def test_move(self, direc):
        p = self.players.characters["player"]
        if p.pos[0]==self.top_left[0] and direc[0]==-1:
            if  self.top_left[0]>0:
                self.top_left = (self.top_left[0]-1, self.top_left[1])
            else:
                return False
        if p.pos[0]==self.top_left[0]+self.view_width-1 and direc[0]==1:
            if self.top_left[0]+self.view_width<self.width:
                self.top_left = (self.top_left[0]+1, self.top_left[1])
            else:
                return False
        if p.pos[1]==self.top_left[1] and direc[1]==-1:
            if self.top_left[1]>0:
                self.top_left=(self.top_left[0], self.top_left[1]-1)
            else:
                return False
        if p.pos[1]==self.top_left[1]+self.view_height-1 and direc[1]==1:
            if self.top_left[1]+self.view_height<self.width:
                self.top_left=(self.top_left[0], self.top_left[1]+1)
            else:
                return False
        new_tile =  self.players.scape[p.pos[0]+direc[0]][p.pos[1]+direc[1]]
        if new_tile!=None:
            return new_tile.collide(direc)
        so = self.landscape.scape[p.pos[0]+direc[0]][p.pos[1]+direc[1]]
        if so!=None:
            return so.collide(direc)
        return True

    def real_render(self, screen):
        screen.fill((0,0,0))
        self.background.render(screen)
        self.landscape.render(screen)
        self.players.render(screen)
        
class layer:
    def __init__(self, board):
        self.height = board.height
        self.width = board.width
        self.view_height = board.view_height
        self.view_width = board.view_width
        self.size = board.size
        self.characters = {}
        self.board=board
        self.scape = [[None for i in range(self.height)] for j in range(self.width)]
        
    def gen_players(self):
        p = person("player", (0,1), self.size, "player.png", None)
        f = person("friend1", (4,3), self.size, "friend.png", None)
        self.add_character(p)
        self.add_character(f)

    def gen_from_arr(self, arr):
        friend_count=0
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if arr[i][j]=='h':
                    h_board = board.from_file("house.b")
                    h = building(str(i)+str(j), (j,i), 100, "house.png", h_board)
                    self.add_character(h)
                if arr[i][j]=='t':
                    t = tree(str(i)+str(j), (j,i), 100, "summer")
                    self.add_character(t)
                if arr[i][j]=='g':
                    g = character(str(i)+str(j), (j,i), 100, "tall_grass.png")
                    self.add_character(g)
                if arr[i][j]=='f':
                    f = person(str(i)+str(j), (j,i), 100, "friend.png")
                    self.add_character(f)

    def gen_landscape(self):
        el_list = ["house.png","tree.png","tall_grass.png"]
        for i in range(self.width):
            for j in range(self.height):
                choice = random.choice(el_list)
                el = character(str(i)+str(j), (i,j), self.board.size, choice)
                self.add_character(el)
    
    def gen_background(self):
        for i in range(self.width):
            for j in range(self.height):
                c = character(str(i)+str(j), (i,j), self.board.size, "background.png")
                self.add_character(c)

    def render(self, screen):
        top_left = self.board.top_left
        for i in range(0,self.view_height):
            for j in range(0,self.view_width):
                current = self.scape[top_left[0]+j][top_left[1]+i]
                if current!=None:
                    current.render((j,i), self.size, screen)

    def add_character(self, char):
        self.scape[char.pos[0]][char.pos[1]]=char
        self.characters[char.name]=char

    def move_character(self, name, direc):
        char = self.characters[name]
        new_pos = (char.pos[0]+direc[0],char.pos[1]+direc[1])
        self.scape[char.pos[0]][char.pos[1]]=None
        self.scape[new_pos[0]][new_pos[1]]=char
        char.pos=new_pos    

 
if __name__=="__main__":
    g = game()
    
