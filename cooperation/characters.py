import pygame
from pygame.locals import *
import events


class character:
    def __init__(self, name, pos, size, image_name):
        self.name=name        
        self.pos=pos
        self.sprite = char_sprite(pos, size, image_name)
        
    def render(self, rpos, size, screen):
        self.sprite.render((rpos[0]*size, rpos[1]*size), size, screen)
    
    def change_image(self, image_name):
        self.sprite.change_image(image_name)
    
    def collide(self,direc):
        return True

class image_library:
    def __init__(self):
        print("Image library created")
        images = open("images.txt")
        self.library = {}
        image_s = images.read()
        for image in image_s.split():
            try:
                self.library[image] = pygame.image.load("./images/"+image)
            except Exception as e:
                print(e)
                print("unable to open: '"+image+"'")
        images.close()

    def get_image(self, name):
        return self.library[name]
  

class char_sprite(pygame.sprite.Sprite):
    image_lib = image_library()

    def __init__(self, pos, size, image):
        super(char_sprite, self).__init__()
        self.size=size
        self.change_image(image)
        self.rect = self.image.get_rect(center=pos)
        self.pos=pos

    def render(self, pos, size, screen):
        #maybe resize the surface
        screen.blit(self.image, (pos[0], pos[1]-self.height+self.size))

    def change_image(self, image_name):
        self.image = char_sprite.image_lib.get_image(image_name)
        rect = self.image.get_rect()
        self.height = int((self.size/rect.width)*rect.height)
        self.image = pygame.transform.scale(self.image, (self.size, self.height)).convert_alpha()

class building(character):
    def __init__(self, name, pos, size, image_name, board):
        super().__init__(name, pos, size, image_name)
        self.board=board
    
    def collide(self, direc):
        if direc!=(0,-1):
            return False
        events.change_board(self.board)
        return False

class tree(character):
    s_map = {"summer":"summer_tree.png", "winter":"winter_tree.png", "fall":"fall_tree.png", "spring":"spring_tree.png"}
    def __init__(self, name, pos, size, season):
        image_name = tree.s_map[season]
        super().__init__(name, pos, size, image_name)
        
    def change_season(self, season):
        image_name = tree.s_map[season]
        self.change_image(image_name)

    def collide(self, direc):
        return False

class person(character):
    def __init__(self, name, pos, size, image_name, menu):
        super().__init__(name, pos, size, image_name)
        self.menu=menu
 
    def collide(self, direc):
        events.new_menu(self.menu)
        return False
