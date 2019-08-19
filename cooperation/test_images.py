import pygame
from pygame.locals import *
from pygame.time import Clock

clock = Clock()
pygame.init()
size=120
screen = pygame.display.set_mode((size*10,size*10))

grass = pygame.image.load("tall_grass.png")
grass = pygame.transform.scale(grass, (size,int(size*5/4))).convert_alpha()
house = pygame.image.load("house.png")
house = pygame.transform.scale(house, (size, int(size*5/4))).convert_alpha()
tree = pygame.image.load("tree.png")
tree = pygame.transform.scale(tree, (size, int(size*5/4))). convert_alpha()

for i in range(0,size*10,size):
    for j in range(0,size*10,size):
        screen.blit(grass, (i,j))
screen.blit(house, (size, size-int(size*1/4)))
screen.blit(tree, (size*2, size-int(size/4)))
for i in range(4,8):
    for j in range(3,6):
        screen.blit(tree, (size*i, size*j-int(size*1/4)))
pygame.display.flip()

running=True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running=False
    clock.tick(3)
