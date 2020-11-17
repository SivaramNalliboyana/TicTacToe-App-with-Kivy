from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.properties import *
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import *
from functools import partial
from kivymd.uix.dialog import MDDialog

class TwoPlayersScreen(Screen):
    pass


class MainApp(MDApp):
    clicked = True
    count = 0
    game_board = {0:'-',1:'-',2:'-',3:'-',4:'-',5:'-',6:'-',7:'-',8:'-'}
    winner = None
    buttons = []

    def showdialog(self,title,text):
        d = MDDialog(auto_dismiss= False,title=title,text=text,size_hint=(.5,.3),text_button_ok="Restart",on_dismiss=self.restart)
        d.open()

    def restart(self,*args):
        for button in self.buttons:
            button.text = ' '
        self.count = 0
        self.game_board = {0: '-', 1: '-', 2: '-', 3: '-', 4: '-', 5: '-', 6: '-', 7: '-', 8: '-'}
        self.winner = None

    def on_start(self):
        for i in range(9):
            grid = self.root.ids['twoplayerscreen'].ids['maingrid']
            b = MDRectangleFlatButton(text=" ",font_size=35,size_hint=(.3,.3),on_release=self.b_clicked,id=str(i))
            self.buttons.append(b)
            grid.add_widget(b)

    def b_clicked(self,button):
        if button.text == " " and self.clicked == True:
            button.text = "X"
            self.game_board[int(button.id)] = button.text
            self.clicked = False
            self.count += 1
            self.check_winner(button)
        elif button.text == " " and self.clicked == False:
            button.text = "O"
            self.game_board[int(button.id)] = button.text
            self.clicked = True
            self.count += 1
            self.check_winner(button)

    def check_winner(self,b):
        row_winner = self.check_rows()
        column_winner = self.check_columns()
        diagonal_winner = self.check_diagonals()
        if row_winner:
            self.showdialog("Congrats",f'Player with {row_winner} won')
            self.winner = row_winner
        if column_winner:
            self.showdialog("Congrats",f'Player with {column_winner} won')
            self.winner = column_winner
        if diagonal_winner:
            self.showdialog("Congrats",f'Player with {diagonal_winner} won')
            self.winner = diagonal_winner
        if self.count == 9 and self.winner is None:
            self.showdialog("No Winner","It is a TIE")

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