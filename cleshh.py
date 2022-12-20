import sys
import traceback

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QLabel)

EMPTY = 0
BLACK = "b"
WHITE = "w"
BOARD_SIZE = (1000, 1000)
CHECKER_FIELD_SIZE = (64, 64)


class Checker(QLabel):

    def __init__(self, game, checker_type, position):
        super().__init__()
        self.game = game
        self.checker_type = checker_type
        self.setFixedSize(CHECKER_FIELD_SIZE[0], CHECKER_FIELD_SIZE[1])
        self.position = position

    def is_empty(self):
        return self.checker_type == EMPTY

    def is_checker(self):
        return self.checker_type == BLACK or self.checker_type == WHITE

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.is_checker() and self.checker_type == self.game.current_checker_type:
            self.game.setWindowTitle("Выберите куда передвинуть шашку")
            self.game.set_current_checker_position(self.position)
            self.game.set_move_flag(True)

        if self.game.move_flag and self.is_empty():
            self.game.set_target_empty_label_position(self.position)
            self.game.move_checker()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.is_checker():
            pass


class Game(QWidget):

    def __init__(self):
        super().__init__()
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.setFixedSize(BOARD_SIZE[0], BOARD_SIZE[1])
        self.show()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.labels = []

        self.init_board()

        self.first_release = False
        self.current_checker_position = None
        self.target_empty_label_position = None
        self.move_flag = False
        self.current_checker_type = WHITE
        self.reset_title()

    def set_move_flag(self, flag):
        self.move_flag = flag

    def next(self):
        self.check_positions()
        if self.current_checker_type == WHITE:
            self.current_checker_type = BLACK
        else:
            self.current_checker_type = WHITE

    def set_current_checker_position(self, position):
        self.current_checker_position = position

    def set_target_empty_label_position(self, position):
        self.target_empty_label_position = position

    def reset_title(self):
        if self.current_checker_type == BLACK:
            self.setWindowTitle("Клещи - ЧЕРНЫЕ")
        else:
            self.setWindowTitle("Клещи - БЕЛЫЕ")

    def check_position_for_lose(self, position):
        # (4,3) (5,2) (5,4)
        try:
            if position[0] != 0:
                if self.board[position[0]][position[1]] == BLACK:
                    if self.board[position[0] - 1][position[1] + 1] == WHITE and \
                            self.board[position[0] + 1][position[1] + 1] == WHITE:
                        return True
                    if self.board[position[0] + 1][position[1] - 1] == WHITE and \
                            self.board[position[0] - 1][position[1] - 1] == WHITE:
                        return True
                    if self.board[position[0] - 1][position[1] - 1] == WHITE and \
                            self.board[position[0] - 1][position[1] + 1] == WHITE:
                        return True
                    if self.board[position[0] + 1][position[1] - 1] == WHITE and \
                            self.board[position[0] + 1][position[1] + 1] == WHITE:
                        return True
                if self.board[position[0]][position[1]] == WHITE:
                    if self.board[position[0] - 1][position[1] + 1] == BLACK and \
                            self.board[position[0] + 1][position[1] + 1] == BLACK:
                        return True
                    if self.board[position[0] + 1][position[1] - 1] == BLACK and \
                            self.board[position[0] - 1][position[1] - 1] == BLACK:
                        return True
                    if self.board[position[0] - 1][position[1] - 1] == BLACK and \
                            self.board[position[0] - 1][position[1] + 1] == BLACK:
                        return True
                    if self.board[position[0] + 1][position[1] - 1] == BLACK and \
                            self.board[position[0] + 1][position[1] + 1] == BLACK:
                        return True
        except IndexError:
            pass
        return False

    def check_positions(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                #print(i, j)
                #print(self.check_position_for_lose((i, j)))
                if self.check_position_for_lose((i, j)):
                    self.board[i][j] = EMPTY

    def move_checker(self):

        if self.current_checker_type == WHITE:
            if self.target_empty_label_position[0] == self.current_checker_position[0] - 1 and (
                    self.target_empty_label_position[1] == self.current_checker_position[1] - 1):
                self.board[self.target_empty_label_position[0]][self.target_empty_label_position[1]] = \
                    self.board[self.current_checker_position[0]][self.current_checker_position[1]]
                self.board[self.current_checker_position[0]][self.current_checker_position[1]] = EMPTY
                self.next()

            if self.target_empty_label_position[0] == self.current_checker_position[0] - 1 and (
                    self.target_empty_label_position[1] == self.current_checker_position[1] + 1):
                self.board[self.target_empty_label_position[0]][self.target_empty_label_position[1]] = \
                    self.board[self.current_checker_position[0]][self.current_checker_position[1]]
                self.board[self.current_checker_position[0]][self.current_checker_position[1]] = EMPTY
                self.next()
        if self.current_checker_type == BLACK:
            if self.target_empty_label_position[0] == self.current_checker_position[0] + 1 and (
                    self.target_empty_label_position[1] == self.current_checker_position[1] + 1):
                self.board[self.target_empty_label_position[0]][self.target_empty_label_position[1]] = \
                    self.board[self.current_checker_position[0]][self.current_checker_position[1]]
                self.board[self.current_checker_position[0]][self.current_checker_position[1]] = EMPTY
                self.next()

            if self.target_empty_label_position[0] == self.current_checker_position[0] + 1 and (
                    self.target_empty_label_position[1] == self.current_checker_position[1] - 1):
                self.board[self.target_empty_label_position[0]][self.target_empty_label_position[1]] = \
                    self.board[self.current_checker_position[0]][self.current_checker_position[1]]
                self.board[self.current_checker_position[0]][self.current_checker_position[1]] = EMPTY
                self.next()

        self.clear_board()
        self.fill_board()
        self.reset_title()
        self.move_flag = False
        self.current_checker_position = None
        self.target_empty_label_position = None

    def init_board(self):
        count = 1
        for i in range(3):
            for j in range(count, 8, 2):
                self.board[i][j] = BLACK
            if count == 1:
                count = 0
            else:
                count = 1

        count = 0
        for i in range(5, 8):
            for j in range(count, 8, 2):
                self.board[i][j] = WHITE
            if count == 1:
                count = 0
            else:
                count = 1
        self.fill_board()

    def fill_board(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == WHITE:
                    label = Checker(self, WHITE, (i, j))
                    pixmap = QPixmap('assets/white.png')
                    label.setPixmap(pixmap)
                    self.labels.append(label)
                    self.grid.addWidget(label, i, j)

                elif self.board[i][j] == BLACK:
                    label = Checker(self, BLACK, (i, j))
                    pixmap = QPixmap('assets/black.png')
                    label.setPixmap(pixmap)
                    self.labels.append(label)
                    self.grid.addWidget(label, i, j)
                else:
                    label = Checker(self, EMPTY, (i, j))
                    pixmap = QPixmap('assets/empty.png')
                    label.setPixmap(pixmap)
                    self.labels.append(label)
                    self.grid.addWidget(label, i, j)

    def clear_board(self):
        for label in self.labels:
            self.grid.removeWidget(label)
        self.labels.clear()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error caught!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()

sys.excepthook = excepthook
app = QtWidgets.QApplication([])
application = Game()
application.show()
sys.exit(app.exec())
