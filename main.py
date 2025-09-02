from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import *
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
import copy
import math


class TwoPlayersScreen(Screen):
    pass


class MainApp(MDApp):
    ai = 'X'
    human = 'O'
    currentplayer = 'human'
    game_board = {0:'-',1:'-',2:'-',3:'-',4:'-',5:'-',6:'-',7:'-',8:'-'}
    buttons = []
    winner = None
    count = 0
    scores = {'X': 10, 'O': -10, 'tie': 0}

    def showdialog(self,title,text):
        pass

    def restart(self,winner,*args):
        s = Snackbar(text=f'Player with {winner} won', font_size=20).show()
        for button in self.buttons:
            button.text = ' '
        self.count = 0
        self.game_board = {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-'}
        self.winner = None

    def on_start(self):
        for i in range(9):
            grid = self.root.ids['twoplayerscreen'].ids['maingrid']
            b = MDRectangleFlatButton(text=" ",font_size=35,size_hint=(.3,.3),on_release=self.b_clicked,padding=i)
            self.buttons.append(b)
            grid.add_widget(b)
        self.computermove()


    def computermove(self):
        bestscore = -math.inf
        bestMove = None
        for move in self.game_board:
            if self.game_board[move] == "-":
                self.game_board[move] = self.ai
                score = self.minimax(self.game_board,0,False)
                self.game_board[move] = '-'
                if score > bestscore:

                    bestscore = score
                    bestMove = move
        self.game_board[bestMove] = self.ai
        self.buttons[bestMove].text = self.ai
        self.count += 1
        self.currentplayer = self.human

    def minimax(self,board,depth,isMaximizing):
        result = self.check_winner()
        if result is not None:
            return self.scores[result]
        if isMaximizing:
            best_score = -math.inf
            for move in self.game_board:
                if self.game_board[move] == "-":
                    self.game_board[move] = self.ai
                    score = self.minimax(self.game_board,depth+1,False)

                    self.game_board[move] = '-'
                    best_score = max(score,best_score)
            return best_score
        else:
            best_score = math.inf
            for move in self.game_board:
                if self.game_board[move] == "-":
                    self.game_board[move] = self.human
                    score = self.minimax(self.game_board, depth + 1, True)
                    self.game_board[move] = '-'
                    best_score = min(score, best_score)
            return best_score

    def b_clicked(self,button):
        if self.currentplayer == self.human:
            self.game_board[button.padding[0]] = self.human
            button.text = self.human
            self.count += 1
            self.currentplayer = self.ai
            self.computermove()

    def check_winner(self):
        row_winner = self.check_rows()
        column_winner = self.check_columns()
        diagonal_winner = self.check_diagonals()
        if row_winner:
            return row_winner
        if column_winner:
            return column_winner
        if diagonal_winner:
            return diagonal_winner

        if self.winner is None and self.count == 9:
            return 'tie'
        if self.winner is not None:
            return self.winner

    def check_rows(self):
        row_1 = self.game_board[0] == self.game_board[1] == self.game_board[2] != "-"
        row_2 = self.game_board[3] == self.game_board[4] == self.game_board[5] != "-"
        row_3 = self.game_board[6] == self.game_board[7] == self.game_board[8] != "-"
        if row_1:
            return self.game_board[0]
        elif row_2:
            return self.game_board[3]
        elif row_3:
            return self.game_board[6]
        else:
            return None

    def check_columns(self):
        column_1 = self.game_board[0] == self.game_board[3] == self.game_board[6] != "-"
        column_2 = self.game_board[1] == self.game_board[4] == self.game_board[7] != "-"
        column_3 = self.game_board[2] == self.game_board[5] == self.game_board[8] != "-"
        if column_1:
            return self.game_board[0]
        elif column_2:
            return self.game_board[1]
        elif column_3:
            return self.game_board[2]
        else:
            return None

    def check_diagonals(self):
        diagonal_1 =self.game_board[0] == self.game_board[4] == self.game_board[8] != "-"
        diagonal_2 = self.game_board[2] == self.game_board[4] == self.game_board[6] != "-"
        if diagonal_1:
            return self.game_board[0]
        elif diagonal_2:
            return self.game_board[2]
        else:
            return None

    def __init__(self):
        Window.size = (400,600)
        super().__init__()


MainApp().run()
