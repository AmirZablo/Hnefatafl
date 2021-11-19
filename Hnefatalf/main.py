import pygame
import hnefatafl.constants as c
from hnefatafl.game import Game
from hnefatafl.board import Board

FPS=60

#Init window
WIN=pygame.display.set_mode((c.width,c.height))
pygame.display.set_caption("Hnefatafl")

def get_row_col_from_mouse(pos):
    x, y= pos
    row= (y-75)//c.square_size
    col= (x-75)//c.square_size

    #Click inside the board
    if 0<=row<=10 and 0<=col<=10:
        return row, col
    else:
        return -1, -1
        

def main():
    run=True
    clock=pygame.time.Clock()
 
    #board=Board()
    game= Game(WIN)

    #Main cycle
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            #Deal with mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if not game.winner:
                    game.select(row,col)
                else:
                    if 186<=pos[0]<=502 and 551<=pos[1]<=618: #Reset button in end game screen
                        game.reset()
                
        
        #Refresh
        game.update()

        

    pygame.display

    pygame.quit()

main()

