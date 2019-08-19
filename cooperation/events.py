import pygame
from pygame.locals import *

CHANGE_BOARD = pygame.USEREVENT + 1
NEW_MENU = pygame.USEREVENT + 2

def change_board(board):
    ev = pygame.event.Event(CHANGE_BOARD, data=board)
    pygame.event.post(ev)
    
def new_menu(menu):
    ev = pygame.event.Event(NEW_MENU, data=menu)
    pygame.event.post(ev)


if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                running=False
            if event.type==KEYDOWN:
                change_board("hello")
            if event.type == CHANGE_BOARD:
                print(event.data)
