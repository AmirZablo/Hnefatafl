from hnefatafl.constants import square_size
import pygame as p

class Piece:
    def __init__(self, row, column, color,is_king):
        self.row=row
        self.column=column
        self.color=color
        self.is_king=is_king
        self.calc_pos()
        
    def calc_pos(self):
        self.x= square_size*self.column+ 75 + square_size//2 #Add margin offset and half of the square
        self.y= square_size*self.row + 75 + square_size//2 #Add margin offset and half of the square

    def draw(self, win):
        if self.is_king:
            p.draw.circle(win,(28.6,18.4,2.7), (self.x,self.y),square_size//2 - 4)
            p.draw.circle(win,self.color, (self.x,self.y),square_size//2 - 6)
            p.draw.circle(win,(28.6,18.4,2.7), (self.x,self.y),square_size//2 - 8)
            p.draw.circle(win,self.color, (self.x,self.y),square_size//2 - 10)

        else:
            p.draw.circle(win,(28.6,18.4,2.7), (self.x,self.y),square_size//2 - 10)
            p.draw.circle(win,self.color, (self.x,self.y),square_size//2 - 12)

    def move(self,row,col):
        self.row=row
        self.column=col
        self.calc_pos()
    
    def __repr__(self): #when print(Piece), it shows the color (for debugging purposes)
        return str(self.color)