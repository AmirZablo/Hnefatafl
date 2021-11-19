from hnefatafl.board import Board
import pygame
import hnefatafl.constants as c

class Game:
    def __init__(self, win):
        self.selected= None
        self.board= Board()
        self.turn= 'black'
        self.valid_moves= []
        self.win= win
        self.winner=None
        
    #Update the screen
    def update(self):
        
        self.win.blit(pygame.image.load('background.png'),(0,0))
        if self.turn=='white' and not self.winner:
            self.win.blit(pygame.image.load('turn_white.png'),(255,10))
        elif self.turn=='black' and not self.winner:
            self.win.blit(pygame.image.load('turn_black.png'),(255,10))

        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if self.winner:
            self.win.blit(pygame.image.load(str(self.winner)+'.png'),(0,0))
        pygame.display.update()

    #Reset the game
    def reset(self):
        self.selected= None
        self.board= Board()
        self.turn= 'black'
        self.valid_moves= []
        self.winner=None

    #Deal with selections (piece or empty square)
    def select(self, row, col):
        if self.selected:
            result=self._move(row, col)
            if not result:
                self.valid_moves=[]
                self.update()
                self.selected= None
                self.select(row, col)

        
        piece=self.board.get_piece(row,col)
        if piece!=0 and piece.color==self.turn:
            self.selected= piece
            self.valid_moves= self.board.get_valid_moves(piece)
            return True
            
        return False

    #Move piece and check captures or game end
    def _move(self, row, col):
        piece=self.board.get_piece(row,col)
        if self.selected and piece==0 and (row,col) in self.valid_moves:
            self.board.move(self.selected,row,col)
            
            #Check captures
            captured_pieces= self.board.captures(self.selected)
            for captured in captured_pieces:
                self.board.remove_piece(captured)

            #Check if game ended
            ended=self.board.game_ended()
            if ended:
                self.declare_winner(ended)

            self.change_turn()


        else:
            return False

        return True

    #Change turn
    def change_turn(self):
        self.valid_moves=[]
        if self.turn=='black':
            self.turn='white'
        else:
            self.turn='black'

    #Draw valid moves for selected piece
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win,c.selec,(col*c.square_size+75+c.square_size//2,row*c.square_size+75+c.square_size//2),5)

    #Set winner
    def declare_winner(self, color):
        self.winner=color