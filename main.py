import sys
import io
import random
import os

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from template import gettemplate


class MyWidget(QWidget):
    def __init__(self, W, H, M, Login="", Password=""):
        # Game state 0 - unknown, 1 - win, -1, lose
        self.Game = 0
        self.field = []
        self.map = []
        # Field size
        self.W = W
        self.H = H
        self.M = M
        self.LoginT = Login
        self.PasswordT = Password
        # Initialisation
        super().__init__()
        # Generate template function
        template = gettemplate(self.W, self.H, "untitled1.ui")
        design = io.StringIO(template)
        uic.loadUi(design, self)
        # Size of the Window when field is generated
        if self.W > 10:
            self.setFixedWidth(500 + (self.W - 10) * 40)
        self.setFixedHeight(270 + self.H * 40)
        # Set to widgets size, number of mines value, login and password
        self.WSize.setValue(self.W)
        self.HSize.setValue(self.H)
        self.MNumber.setValue(self.M)
        self.Login.setText(self.LoginT)
        self.Password.setText(self.PasswordT)
        # Buttons connect with functions
        self.Play.clicked.connect(self.generate_field)
        self.NewGame.clicked.connect(self.restart)
        self.Save.clicked.connect(self.save)
        self.Load.clicked.connect(self.load)

    def generate_field(self):  # generating field function
        # Get from input size and number of mines
        W1 = self.WSize.value()
        H1 = self.HSize.value()
        M1 = self.MNumber.value()
        # Checking if W and H is correct
        if W1 == 0 or H1 == 0:
            print("Input size of the field!!\n")
        elif M1 > H1 * W1 or M1 < 1:
            print("Input nuber of mines!!\n")
        else:
            # Create field of the game
            self.close()
            self.__init__(W1, H1, M1, self.Login.toPlainText(), self.Password.toPlainText())
            self.Play.setText("Update")
            self.show()
            self.start_game(W1, H1, M1)

    def restart(self):  # restarting function
        self.close()
        self.__init__(0, 0, 1)
        self.Play.setText("Play")
        self.show()

    def start_game(self, W, H, M):  # starting of the game function
        self.Game = 0  # Game state -> 0
        self.flag = 0  # flag of genetating field
        # create empty field and map
        self.field = []
        self.map = []
        for _ in range(W):
            map1 = []
            field1 = []
            for i in range(H):
                map1.append(0)
                field1.append(".")
            self.map.append(map1)
            self.field.append(field1)
        # connect field with button from design template
        for i in range(self.W):
            for j in range(self.H):
                name = "B" + str(i) + "B" + str(j)
                self.findChild(QPushButton, name).clicked.connect(self.Player)
                self.findChild(QPushButton, name).setStyleSheet('QPushButton {background-color: #3371EF}')
                self.findChild(QPushButton, name).i = i
                self.findChild(QPushButton, name).j = j

    def end_game(self):  # ending of the game function
        # when the game is ended we see all the fied -> show field
        for i in range(self.W):
            for j in range(self.H):
                self.field[i][j] = " "

    def countmines(self, i, j):  # counting mines for field function
        c = 0
        if i == 0 and j == 0:
            if self.map[i + 1][j + 1] == -1:
                c += 1
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            return c
        elif i == self.W - 1 and j == self.H - 1:
            if self.map[i - 1][j - 1] == -1:
                c += 1
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            return c
        elif i == 0 and j == self.H - 1:
            if self.map[i + 1][j - 1] == -1:
                c += 1
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            return c
        elif i == self.W - 1 and j == 0:
            if self.map[i - 1][j + 1] == -1:
                c += 1
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            return c
        elif i == 0:
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            if self.map[i + 1][j + 1] == -1:
                c += 1
            if self.map[i + 1][j - 1] == -1:
                c += 1
            return c
        elif j == 0:
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i + 1][j + 1] == -1:
                c += 1
            if self.map[i - 1][j + 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            return c
        elif i == self.W - 1:
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i - 1][j + 1] == -1:
                c += 1
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            if self.map[i - 1][j - 1] == -1:
                c += 1
            return c
        elif j == self.H - 1:
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i + 1][j - 1] == -1:
                c += 1
            if self.map[i - 1][j - 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            return c
        else:
            if self.map[i][j + 1] == -1:
                c += 1
            if self.map[i + 1][j + 1] == -1:
                c += 1
            if self.map[i - 1][j + 1] == -1:
                c += 1
            if self.map[i + 1][j] == -1:
                c += 1
            if self.map[i - 1][j] == -1:
                c += 1
            if self.map[i][j - 1] == -1:
                c += 1
            if self.map[i + 1][j - 1] == -1:
                c += 1
            if self.map[i - 1][j - 1] == -1:
                c += 1
            return c

    def genMines(self, a, b):  # fill with mines empty field function
        # checking that num of mines less than number of field cells
        if self.M > self.W * self.H - 1:
            return False
        # random position of mines in the cell (field which was indicated first can't be a mine)
        for im in range(self.M):
            a1 = random.randint(0, self.W - 1)
            b1 = random.randint(0, self.H - 1)
            while (a == a1 and b == b1) or self.map[a1][b1] == -1:
                a1 = random.randint(0, self.W - 1)
                b1 = random.randint(0, self.H - 1)
            self.map[a1][b1] = -1
        # show first cell
        self.map[a][b] = 0
        # count mines in other sell, fill out map
        for i1 in range(self.W):
            for j1 in range(self.H):
                if self.map[i1][j1] == 0:
                    self.map[i1][j1] = self.countmines(i1, j1)
        return True

    def ShowBtn(self):  # showing first button function
        value = str(self.map[self.sender().i][self.sender().j])
        if value == "-1":
            self.sender().setText("*")
            self.field[self.sender().i][self.sender().j] = " "
            self.sender().setStyleSheet('QPushButton {background-color: #FF0000}')
            self.end_game()
        elif value == "0":
            self.sender().setText("_")
            self.field[self.sender().i][self.sender().j] = " "
            self.sender().setStyleSheet('QPushButton {background-color: #FFFFFF}')
        else:
            self.sender().setText(value)
            self.field[self.sender().i][self.sender().j] = " "
            self.sender().setStyleSheet('QPushButton {color: #FF0000}')

    def ShowBtn1(self, Btn):  # showing button function
        value = str(self.map[Btn.i][Btn.j])
        if value == "-1":
            Btn.setText("*")
            self.field[self.sender().i][self.sender().j] = " "
            Btn.setStyleSheet('QPushButton {background-color: #FF0000}')
            self.end_game()
        elif value == "0":
            Btn.setText("_")
            self.field[self.sender().i][self.sender().j] = " "
            Btn.setStyleSheet('QPushButton {background-color: #FFFFFF}')
        else:
            Btn.setText(value)
            self.field[self.sender().i][self.sender().j] = " "
            Btn.setStyleSheet('QPushButton {color: #FF0000}')

    def Player(self):
        if self.Game != 0:
            return
        if self.flag == 0:
            if self.genMines(self.sender().i, self.sender().j):
                self.flag = 1
        a = self.sender().i
        b = self.sender().j
        self.ShowBtn()
        self.openzeroes(a, b)
        if self.map[a][b] == -1:
            self.end_game()
            for i in range(self.W):
                for j in range(self.H):
                    name = "B" + str(i) + "B" + str(j)
                    self.ShowBtn1(self.findChild(QPushButton, name))
        elif self.map[a][b] == 0:
            self.field[a][b] = " "
            for i in range(self.W):
                for j in range(self.H):
                    if self.field[i][j] == " ":
                        name = "B" + str(i) + "B" + str(j)
                        self.ShowBtn1(self.findChild(QPushButton, name))
        else:
            self.field[a][b] = " "
        self.Game = self.CheckWinning()
        if self.Game == -1:
            self.Status.setText("You lose(")
        if self.Game == 1:
            self.Status.setText("You win)!!")

    def CheckWinning(self): # checking the state of the game
        for i in range(self.W):
            for j in range(self.H):
                if self.field[i][j] == " " and self.map[i][j] == -1:
                    return -1
        for i in range(self.W):
            for j in range(self.H):
                if self.field[i][j] == "." and self.map[i][j] != -1:
                    return 0
        return 1

    def cango(self, a, b):
        if a < self.W and b < self.H and a > -1 and b > -1:
            return True
        return False

    def CheckToOpen(self, a, b):
        if self.map[a][b] != -1 and self.field[a][b] != " ":
            self.field[a][b] = " "
            if self.map[a][b] == 0:
                self.openzeroes(a, b)

    def openzeroes(self, a, b):
        if self.cango(a + 1, b):
            self.CheckToOpen(a + 1, b)
        if self.cango(a - 1, b):
            self.CheckToOpen(a - 1, b)
        if self.cango(a, b - 1):
            self.CheckToOpen(a, b - 1)
        if self.cango(a, b + 1):
            self.CheckToOpen(a, b + 1)

    def save(self):
        Login = self.Login.toPlainText()
        Password = self.Password.toPlainText()
        if (Login == "" and Password == "") or (Login == " " and Password == " "):
            print("we can't save your game, input your login and password\n")
        filename = "accounts/last_game(" + Login + ").txt"
        if os.path.isfile(filename) == True:
            text = open(filename, "r").read()
            passwf = text[:text.find("\n")]
            if passwf != Password:
                print("Please, choose another login!! this user is already exists\n")
                return
        savefile = open(filename, "w")
        size = str(self.W) + " " + str(self.H) + " " + str(self.M) + "\n"
        field = "Field:"
        for i in range(self.W):
            for j in range(self.H):
                field += str(self.field[i][j]) + ";"
        map = "Map:"
        for i in range(self.W):
            for j in range(self.H):
                map += str(self.map[i][j]) + " "
        savefile.write(Password + "\n" + size + field + "\n" + map)
        print(f"You saved your game with login: {self.LoginT})\n")

    def load(self):
        Login = self.Login.toPlainText()
        Password = self.Password.toPlainText()
        filename = "accounts/last_game(" + Login + ").txt"
        if os.path.isfile(filename) == False:
            print("Can't open file, no Login!!\n")
            return
        loadfile = open(filename, "r")
        text = loadfile.read()
        if text == "":
            return
        passwf = text[:text.find("\n")]
        if passwf != Password:
            print("Incorrect login or password!! Try again please)\n")
            return

        text = text[text.find("\n") + 1:]
        WSize, HSize, MNum = [int(x) for x in text[:text.find("\n")].split(" ")]

        self.close()
        self.__init__(WSize, HSize, MNum, Login, Password)
        self.Play.setText("Play")
        self.show()

        field = text[text.find("Field") + 6:text.find("\nMap:")].split(";")
        self.field = []
        for i in range(WSize):
            field1 = []
            for j in range(HSize):
                field1.append("!")
            self.field.append(field1)
        for i in range(WSize):
            for j in range(HSize):
                self.field[i][j] = field[i * WSize + j]

        map = text[text.find("Map:") + 4:].split(" ")
        self.map = []
        for i in range(WSize):
            map1 = []
            for j in range(HSize):
                map1.append("!")
            self.map.append(map1)
        for i in range(WSize):
            for j in range(HSize):
                self.map[i][j] = int(map[i * WSize + j])

        self.flag = 1

        for i in range(self.W):
            for j in range(self.H):
                name = "B" + str(i) + "B" + str(j)
                self.findChild(QPushButton, name).clicked.connect(self.Player)
                if self.field[i][j] == '.':
                    self.findChild(QPushButton, name).setStyleSheet('QPushButton {background-color: #3371EF}')
                    self.findChild(QPushButton, name).setText(".")
                elif self.map[i][j] == -1:
                    self.findChild(QPushButton, name).setStyleSheet('QPushButton {background-color: #FF0000}')
                    self.findChild(QPushButton, name).setText("*")
                elif self.map[i][j] == 0:
                    self.findChild(QPushButton, name).setText("_")
                    self.findChild(QPushButton, name).setStyleSheet('QPushButton {background-color: #FFFFFF}')
                else:
                    self.findChild(QPushButton, name).setText(str(self.map[i][j]))
                    self.findChild(QPushButton, name).setStyleSheet('QPushButton {color: #FF0000}')
                self.findChild(QPushButton, name).i = i
                self.findChild(QPushButton, name).j = j

        self.Game = self.CheckWinning()
        if self.Game == -1:
            self.Status.setText("Game is already ended(")
        elif self.Game == 1:
            self.Status.setText("Game is already won)")


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget(0, 0, 1)
    ex.show()
    sys.exit(app.exec())
