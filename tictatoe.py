import sys
import copy
import random
# import numpy as np
import pygame

from const import *

# PYGAME SET UP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

# -- CLASSES --
class Board:
    def __init__(self):
            # self.squares = np.zero((ROWS, COLS))
            self.squares = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            self.empty_sqr = self.squares
            self.marked_sqr = 0
            # print(self.squares)
            # self.mark_sqr(1,1,2)
            # print(self.squares)


    def final_state(self):
        '''
        return 0 if there is no win yet
        return 1 if player 1 wins
        return 2 if player 2 wins
        ''' 

            # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
            
             # horiontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[0][col]
            
       # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[1][1]
        
        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[1][1]
        # no win yet
        return 0

    def mark_sqr(self,row,col,player):
        self.squares[row][col] =  player 
        self.marked_sqr += 1

    def empty_sqr(self,row, col):
        return self.squares[row][col] == 0  


    def get_empty_sqrs(self):
        empty__sqrs = []
        for row in range(ROWS):
            for col in range(COLS): 
                if self.empty_sqr(row,col):
                    empty__sqrs.append((row,col))

        return empty__sqrs            
    def is_full(self):
        return  self.marked_sqr == 9 


    def isEmpty(self):
        return self.marked_sqr == 0  

class AI:
    def __init__(self,level=0,player=2):
        self.level = level
        self.player = player

    def rnd_choice(self, board):
        empty__sqrs = board.get_empty_sqrs()
        idy = random.randrange(0,len(empty__sqrs))

        return empty__sqrs(idy)  #(row, col)
    
    def minimal(self,board,making):
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None #eval , move
        
        # player 2 wins
        if case == 2:
            return -1, None
        
        # draw
        elif board.is_full():
            return 0 , None
        
        if making:
            may_eval = -100
            best_move = None
            empty__sqr = board.get_empty_sqrs()

            for (row,col) in empty__sqr:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimal(temp_board,False)[0]
                if eval < may_eval:
                    may_eval = eval
                    best_move = (row,col)

            return may_eval, best_move  
            

        elif not making:
            min_eval = 100
            best_move = None
            empty__sqr = board.get_empty_sqrs()

            for (row,col) in empty__sqr:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimal(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)

            return min_eval, best_move        

    def eval(self,main_board):
        if self.level == 0:
            # random choice  
            eval = 'random'
            move = self.rnd_choice(main_board)
        else:
            # minimum algorithm choice
            eval, move = self.minimal(main_board,False)

        print(f'AI has chosen to mark the square in pass{move} with an eval of {eval}')    

        return move #(row,col)
 
class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  #1-cross 2-circles
        self.gamemode = 'ai' #pvp or ai
        self.running = True
        self.show_lines()

    def make_move(self, row, col): 
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.change_player()
    def show_lines(self):
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen,LINE_COLOR, (SIQSIC,0),(SIQSIC,HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR, (WIDTH - SIQSIC,0),(WIDTH - SIQSIC, HEIGHT), LINE_WIDTH)

        # horiontal
        pygame.draw.line(screen,LINE_COLOR, (0,SIQSIC),(WIDTH,SIQSIC), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR, (0, HEIGHT - SIQSIC),(WIDTH,HEIGHT - SIQSIC), LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SIQSIC + OFFSET, row * SIQSIC + OFFSET)
            end_desc = (col * SIQSIC + SIQSIC - OFFSET, row * SIQSIC + SIQSIC - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR,start_desc,end_desc, CROSS_WIDTH)
            
            # asc line
            start_asc = (col * SIQSIC + OFFSET, row * SIQSIC +SIQSIC - OFFSET)
            end_asc = (col * SIQSIC + SIQSIC - OFFSET, row * SIQSIC +  OFFSET)
            pygame.draw.line(screen, CROSS_COLOR,start_asc,end_asc, CROSS_WIDTH)
        elif  self.player == 2:
            # draw circle
            center = (col * SIQSIC + SIQSIC // 2, row * SIQSIC +  SIQSIC // 2)
            pygame.draw.circle(screen, CIRC_COLOR,center,RADIUS,CIRC_WIDTH)


    def change_player(self):
        self.player = self.player % 2 + 1

    def reset(self):
        self.__init__()




def change_gamemode(self):
    self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp' #or
    # if self.gamemode == 'pvp': 
    #     self.gamemode = 'ai'
    # else: 
    #     self.gamemode = 'pvp'

def main():
    # object
    game = Game()
    board= game.board
    ai = game.ai
    # main loop
    while True:

        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] //SIQSIC
                col = pos[0] //SIQSIC
                # print(row,col)

                if board.empty_sqr(row,col):
                    game.make_move(row,col)
                #    board.mark_sqr(row,col, game.player)
                #    game.draw_fig(row,col)
                #    game.change_player()
                    # print(board.squares)

                # game.board.mark_sqr(row,col,1)
                # print(game.board.squares)
                if event.type == pygame.KEYDOWN:
                    # g-gamemode
                    if event.key == pygame.K_g:
                        game.change_gamemode()

                    # r-restart
                    if event.key == pygame.K_r:
                        game.reset()
                        board = game.board
                        ai = game.ai
                    # 0 - random ai
                    if event.key == pygame.K_0:
                        ai.level = 0

                        # 1- random ai
                    if event.key == pygame.K_1:
                        ai.level = 1  
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
                # update the screen 
            pygame.display.update()  
            # ai method
            row,col = ai.eval(board)
            board.mark_sqr(row,col, ai.player)
            game.draw_fig(row,col)
            game.change_player()


        pygame.display.update()        

main()    
