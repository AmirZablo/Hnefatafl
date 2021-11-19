import pygame
import hnefatafl.constants as c
from .piece import Piece

class Board:
    def __init__(self):
        self.board=[[0,0,0,Piece(0,3,'black',False),Piece(0,4,'black',False),Piece(0,5,'black',False),Piece(0,6,'black',False),Piece(0,7,'black',False),0,0,0],
        [0,0,0,0,0,Piece(1,5,'black',False),0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0],
        [Piece(3,0,'black',False),0,0,0,0,Piece(3,5,'white',False),0,0,0,0,Piece(3,10,'black',False)],
        [Piece(4,0,'black',False),0,0,0,Piece(4,4,'white',False),Piece(4,5,'white',False),Piece(4,6,'white',False),0,0,0,Piece(4,10,'black',False)],
        [Piece(5,0,'black',False),Piece(5,1,'black',False),0,Piece(5,3,'white',False),Piece(5,4,'white',False),Piece(5,5,'white',True),Piece(5,6,'white',False),Piece(5,7,'white',False),0,Piece(5,9,'black',False),Piece(5,10,'black',False)],
        [Piece(6,0,'black',False),0,0,0,Piece(6,4,'white',False),Piece(6,5,'white',False),Piece(6,6,'white',False),0,0,0,Piece(6,10,'black',False)],
        [Piece(7,0,'black',False),0,0,0,0,Piece(7,5,'white',False),0,0,0,0,Piece(7,10,'black',False)],
        [0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,Piece(9,5,'black',False),0,0,0,0,0],
        [0,0,0,Piece(10,3,'black',False),Piece(10,4,'black',False),Piece(10,5,'black',False),Piece(10,6,'black',False),Piece(10,7,'black',False),0,0,0]]
        self.white_left=12 #without counting the king
        self.black_left=24
        self.king_captured=False
        
    #Draw pieces on the board
    def draw(self, win):
        for row in range(c.rows):
            for col in range(c.cols):
                piece=self.board[row][col]
                
                if piece!=0:
                    piece.draw(win)

    #Move the pieces
    def move(self, piece, row, col):
        self.board[piece.row][piece.column], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.column] 
        piece.move(row,col)

    #Get selected piece 
    def get_piece(self, row, col):
        return self.board[row][col]

    #Get valid moves in every direction
    def get_valid_moves(self, piece):
        moves=[]

        #Check up
        row_candid=piece.row
        col_candid=piece.column
        while row_candid>0:
            row_candid-=1
            if self.board[row_candid][col_candid]==0:
                moves.append((row_candid,col_candid))
            else:
                break
        
        #Check down
        row_candid=piece.row
        col_candid=piece.column
        while row_candid<10:
            row_candid+=1
            if self.board[row_candid][col_candid]==0:
                moves.append((row_candid,col_candid))
            else:
                break

        #Check left
        row_candid=piece.row
        col_candid=piece.column
        while col_candid>0:
            col_candid-=1
            if self.board[row_candid][col_candid]==0:
                moves.append((row_candid,col_candid))
            else:
                break

        #Check right
        row_candid=piece.row
        col_candid=piece.column
        while col_candid<10:
            col_candid+=1
            if self.board[row_candid][col_candid]==0:
                moves.append((row_candid,col_candid))
            else:
                break
        
        #Check king-exclusive moves
        if not piece.is_king:
            if (0,0) in moves:
                moves.remove((0,0))
            if (0,10) in moves:
                moves.remove((0,10))
            if (10,0) in moves:
                moves.remove((10,0))
            if (10,10) in moves:
                moves.remove((10,10))
            if (5,5) in moves:
                moves.remove((5,5))

        return moves

    #Check piece captured (king capture is dealt with in the game_ended function)
    def captures(self, piece):
        row=piece.row
        col=piece.column
        color=piece.color
        row_king, col_king= self.king_position()
        captured=[]

        if self.game_ended():
            return []

        #Upward captures
        if row >= 2:
            if self.board[row-1][col]!=0 and self.board[row-1][col].color!=color: 
                if not self.board[row-1][col].is_king: #there is an enemy up, and it is not king
                    if self.board[row-2][col]!=0 and self.board[row-2][col].color==color:
                        captured.append(self.board[row-1][col])
                    elif (row==2 and col==0) or (row==2 and col==10): #capture with help of a corner
                        captured.append(self.board[row-1][col])
                    elif (row_king!=5 or col_king!=5) and (row==7 and col==5): #capture with help of the throne (only if king is not there)
                        captured.append(self.board[row-1][col])
                
        #Right captures
        if col <= 8:
            if self.board[row][col+1]!=0 and self.board[row][col+1].color!=color: 
                if not self.board[row][col+1].is_king: #there is an enemy right, and it is not king
                    if self.board[row][col+2]!=0 and self.board[row][col+2].color==color:
                        captured.append(self.board[row][col+1])
                    elif (row==0 and col==8) or (row==10 and col==8): #capture with help of a corner
                        captured.append(self.board[row][col+1])
                    elif (row_king!=5 or col_king!=5) and (row==5 and col==3): #capture with help of the throne (only if king is not there)
                        captured.append(self.board[row][col+1])

        #Downward captures
        if row <= 8:
            if self.board[row+1][col]!=0 and self.board[row+1][col].color!=color: 
                if not self.board[row+1][col].is_king: #there is an enemy down, and it is not king
                    if self.board[row+2][col]!=0 and self.board[row+2][col].color==color:
                        captured.append(self.board[row+1][col])
                    elif (row==8 and col==0) or (row==8 and col==10): #capture with help of a corner
                        captured.append(self.board[row+1][col])
                    elif (row_king!=5 or col_king!=5) and (row==3 and col==5): #capture with help of the throne (only if king is not there)
                        captured.append(self.board[row+1][col])

        #Left captures
        if col >= 2:
            if self.board[row][col-1]!=0 and self.board[row][col-1].color!=color: 
                if not self.board[row][col-1].is_king: #there is an enemy left, and it is not king
                    if self.board[row][col-2]!=0 and self.board[row][col-2].color==color:
                        captured.append(self.board[row][col-1])
                    elif (row==0 and col==2) or (row==10 and col==2): #capture with help of a corner
                        captured.append(self.board[row][col-1])
                    elif (row_king!=5 or col_king!=5) and (row==5 and col==7): #capture with help of the throne (only if king is not there)
                        captured.append(self.board[row][col-1])

        return captured

    #Remove piece
    def remove_piece(self, piece):
        self.board[piece.row][piece.column]= 0
        piece.move(-1,-1) #for debugging purposes

    #Check if game is over
    def game_ended(self):
        row_king, col_king = self.king_position()
        
        #Check if king reached a corner
        if self.board[0][0]!=0 or self.board[0][10]!=0 or self.board[10][0]!=0 or self.board[10][10]!=0:
            return "White"

        #Check if king is surrounded by enemies (or throne)
        if row_king != 0 and row_king != 10 and col_king != 0 and col_king != 10: #King cannot be captured against a side
            neighbors=[self.board[row_king-1][col_king], self.board[row_king][col_king+1], self.board[row_king+1][col_king], self.board[row_king][col_king-1]]
            enemy_neighbors=0
            for n in neighbors:
                if n!=0 and n.color=='black':
                        enemy_neighbors+=1

            #Check if king is next to the throne
            if (row_king==5 and col_king==4) or (row_king==5 and col_king==6) or (row_king==4 and col_king==5) or (row_king==6 and col_king==5):
                enemy_neighbors+=1

            if enemy_neighbors==4:
                return "Black"

        #Check if king and all theremaining defenders are surrounded
        mins={'row':{'row':11,'color':''},'col':{'col':11,'color':''}}
        maxs={'row':{'row':-1,'color':''},'col':{'col':-1,'color':''}}
        black_pos=[]

        for i in range(c.rows):
            for j in range(c.cols):
                if self.board[i][j]!=0:
                    if self.board[i][j].color=='black':
                        black_pos.append((self.board[i][j].row, self.board[i][j].column))

                    if i<mins['row']['row']:
                        mins['row']['row']=i
                        mins['row']['color']=self.board[i][j].color
                    if j<mins['col']['col']:
                        mins['col']['col']=j
                        mins['col']['color']=self.board[i][j].color
                    if i>maxs['row']['row']:
                        maxs['row']['row']=i
                        maxs['row']['color']=self.board[i][j].color
                    if j>maxs['col']['col']:
                        maxs['col']['col']=j
                        maxs['col']['color']=self.board[i][j].color

        if mins['row']['color']=='black' and mins['col']['color']=='black' and maxs['row']['color']=='black' and maxs['col']['color']=='black': #Outer piece in each direction is black
            #check if each white piece is enclosed in a closed path of black pieces
            black_won=True
            for i in range(c.rows):
                for j in range(c.cols):
                    if self.board[i][j] != 0 and self.board[i][j].color=='white':
                        flood_board=[[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0]]
                        self.flood_fill(flood_board,i,j)
                        if (1 in flood_board[0][:]) or (1 in flood_board[10][:]) or (1 in flood_board[:][0]) or (1 in flood_board[:][10]):
                            black_won=False
            
            if black_won:
                return "Black"

        #Check if a color has no legal moves
        white_moves=[]
        black_moves=[]
        for i in range(c.rows):
            for j in range(c.cols):
                if self.board[i][j]!=0:
                    if self.board[i][j].color=='white':
                        new_white_moves=self.get_valid_moves(self.board[i][j])
                        white_moves.extend(new_white_moves)
                    
                    else:
                        new_black_moves=self.get_valid_moves(self.board[i][j])
                        black_moves.extend(new_black_moves)

                if len(white_moves)>0 and len(black_moves)>0:
                    return None
        
        if len(black_moves)==0:
            return "White"
        else:
            return "Black"
            

    def king_position(self):
        row_king=-1
        col_king=-1
        for row in range(11):
            for col in range(11):
                if self.board[row][col] != 0:
                    if self.board[row][col].is_king:
                        row_king, col_king = row, col
                        break
            if row_king != -1 and col_king != -1:
                break
        
        return row_king, col_king

    def flood_fill(self, flood_board,row,col):
        if (self.board[row][col]!=0 and self.board[row][col].color=='black') or flood_board[row][col]==1:
            return

        flood_board[row][col]=1

        if row<10:
            self.flood_fill(flood_board,row+1,col)
        if row>0:
            self.flood_fill(flood_board,row-1,col)
        if col<10:
            self.flood_fill(flood_board,row,col+1)
        if col>0:
            self.flood_fill(flood_board,row,col-1)
                
 
    
        
        


    
