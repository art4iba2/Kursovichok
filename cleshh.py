import random
import sys
import traceback

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QLabel, QMessageBox)
from menu import Ui_Form

BLACK = "b"
WHITE = "w"
BOARD_SIZE = (800, 800)
CHECKER_FIELD_SIZE = (64, 64)


class Menu(QWidget, Ui_Form):

    def __init__(self):
        super(Menu, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.game = None
        self.exitButton.clicked.connect(self.close)
        self.singlePlayButton.clicked.connect(self.single_play)
        self.computerPlayButton.clicked.connect(self.computer_play)

    def single_play(self):
        self.game = Game()
        self.game.show()
        self.close()

    def computer_play(self):
        self.game = Game(mode=Game.COMPUTER_MODE)
        self.game.show()
        self.close()


class Checker(QLabel):

    def __init__(self, game, checker_type, position, queen_flag=False):
        super().__init__()
        self.game = game
        self.checker_type = checker_type
        self.position = position
        self.queen_flag = queen_flag
        self.setFixedSize(CHECKER_FIELD_SIZE[0], CHECKER_FIELD_SIZE[1])
        self.config()

    def config(self):
        if self.is_white():
            if self.is_queen():
                self.setPixmap(QPixmap('assets/WHITE-QUEEN.png'))
            elif self.game.current_player == WHITE:
                self.setPixmap(QPixmap('assets/WHITE-ACTIVE.png'))
            else:
                self.setPixmap(QPixmap('assets/WHITE.png'))
        elif self.is_black():
            if self.is_queen():
                self.setPixmap(QPixmap('assets/BLACK-QUEEN.png'))
            elif self.game.current_player == BLACK:
                self.setPixmap(QPixmap('assets/BLACK-ACTIVE.png'))
            else:
                self.setPixmap(QPixmap('assets/BLACK.png'))
        else:
            self.setPixmap(QPixmap('assets/EMPTY.png'))

    def is_white(self):
        return self.checker_type == WHITE

    def is_black(self):
        return self.checker_type == BLACK

    def is_empty(self):
        return self.checker_type is None

    def is_queen(self):
        return self.queen_flag

    def is_checker(self):
        return self.checker_type in [BLACK, WHITE]

    def get_queen_moves_for_position(self):
        moves = []
        last_position = self.position
        for i in range(4):
            last_position = (last_position[0] + 1, last_position[1] - 1)
            if self.game.check_cell_for_move(last_position):
                moves.append(last_position)
        last_position = self.position
        for i in range(4):
            last_position = (last_position[0] - 1, last_position[1] + 1)
            if self.game.check_cell_for_move(last_position):
                moves.append(last_position)
        last_position = self.position
        for i in range(4):
            last_position = (last_position[0] + 1, last_position[1] + 1)
            if self.game.check_cell_for_move(last_position):
                moves.append(last_position)
        last_position = self.position
        for i in range(4):
            last_position = (last_position[0] - 1, last_position[1] - 1)
            if self.game.check_cell_for_move(last_position):
                moves.append(last_position)
        return moves

    def get_available_moves(self):
        available_moves = []
        if self.is_queen():
            return self.get_queen_moves_for_position()
        if self.is_white():
            new_position = (self.position[0] - 1, self.position[1] - 1)
            if self.game.check_cell_for_move(new_position):
                available_moves.append(new_position)
            new_position = (self.position[0] - 1, self.position[1] + 1)
            if self.game.check_cell_for_move(new_position):
                available_moves.append(new_position)
        elif self.is_black():
            new_position = (self.position[0] + 1, self.position[1] + 1)
            if self.game.check_cell_for_move(new_position):
                available_moves.append(new_position)
            new_position = (self.position[0] + 1, self.position[1] - 1)
            if self.game.check_cell_for_move(new_position):
                available_moves.append(new_position)
        return available_moves

    def check_for_queen_mode_activate(self):
        if self.is_black():
            if self.position[0] == 7:
                self.queen_flag = True
        elif self.is_white():
            if self.position[0] == 0:
                self.queen_flag = True

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.is_checker() and self.checker_type == self.game.current_player:
            self.game.setWindowTitle("Выберите куда передвинуть шашку")
            self.game.set_current_checker(self)
            self.game.set_move_flag(True)

        if self.game.move_flag and self.is_empty():
            self.game.set_target_position(self.position)
            self.game.player_move()


class Game(QWidget):
    SINGLE_MODE = "SINGLE"
    COMPUTER_MODE = "COMPUTER"
    menu = None
    msg = None

    def __init__(self, mode=SINGLE_MODE):
        super().__init__()
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setFixedSize(BOARD_SIZE[0], BOARD_SIZE[1])
        self.mode = mode
        self.current_player = WHITE
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.init_board()
        self.fill_board()

        self.first_release = False
        self.current_checker = None
        self.target_position = None
        self.move_flag = False
        self.reset_title()

    def check_cell_for_move(self, position):
        try:
            if position[0] < 0 or position[1] < 0:
                return False
            if self.board[position[0]][position[1]].is_empty():
                return True
        except IndexError:
            pass
        return False

    def init_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = Checker(self, None, (i, j))
        counter = 1
        for i in range(3):
            for j in range(counter, 8, 2):
                self.board[i][j] = Checker(self, BLACK, (i, j))
            if counter == 1:
                counter = 0
            else:
                counter = 1
        counter = 0
        for i in range(5, 8):
            for j in range(counter, 8, 2):
                self.board[i][j] = Checker(self, WHITE, (i, j))
            if counter == 1:
                counter = 0
            else:
                counter = 1

    def fill_board(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j].config()
                self.grid.addWidget(self.board[i][j], i, j)

    def clear_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.grid.removeWidget(self.board[i][j])

    def reset_title(self):
        if self.current_player == BLACK:
            self.setWindowTitle("Клещи - ЧЕРНЫЕ")
        else:
            self.setWindowTitle("Клещи - БЕЛЫЕ")

    def set_move_flag(self, flag):
        self.move_flag = flag

    def set_current_checker(self, checker):
        self.current_checker = checker

    def set_target_position(self, position):
        self.target_position = position

    def next_player(self):
        if self.current_player == WHITE:
            self.current_player = BLACK
        else:
            self.current_player = WHITE
        if self.mode == self.COMPUTER_MODE and self.current_player == BLACK:
            self.computer_move()

    def check_win(self):
        black_count = 0
        white_count = 0
        for line in self.board:
            for checker in line:
                if checker.is_black():
                    black_count += 1
                elif checker.is_white():
                    white_count += 1
        if black_count == 0:
            self.alert("Победили белые!")
            return
        if white_count == 0:
            self.alert("Победили черные!")
            return

        white_flag = True
        black_flag = True
        for line in self.board:
            for checker in line:
                if checker.is_black() and black_flag:
                    if len(checker.get_available_moves()) > 0:
                        black_flag = False
                elif checker.is_white() and white_flag:
                    if len(checker.get_available_moves()) > 0:
                        white_flag = False

        if black_flag:
            self.alert("Победили белые!")
            return
        if white_flag:
            self.alert("Победили черные!")
            return

    def refresh_after_move(self):
        self.clear_board()
        self.fill_board()
        self.reset_title()
        self.move_flag = False
        self.current_checker = None
        self.target_position = None
        self.check_win()

    def computer_move(self):
        computer_checkers = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].is_black():
                    computer_checkers.append(self.board[i][j])
        random.shuffle(computer_checkers)
        for checker in computer_checkers:
            available_moves = checker.get_available_moves()
            if len(available_moves) > 0:
                move = random.choice(available_moves)
                try:
                    if self.board[move[0]][move[1]].is_empty():
                        self.board[move[0]][move[1]] = checker
                        self.board[checker.position[0]][checker.position[1]] = Checker(self, None, (
                            checker.position[0], checker.position[1]))
                        checker.position = (move[0], move[1])
                        self.check_checker_lose(checker.position)
                        checker.check_for_queen_mode_activate()
                        self.refresh_after_move()
                        self.next_player()
                        return
                except IndexError:
                    pass

    def check_checker_lose(self, position):
        need_check_positions = [(position[0], position[1] - 1), (position[0], position[1] + 1),
                                (position[0] - 1, position[1] - 1), (position[0] - 1, position[1]),
                                (position[0] - 1, position[1] + 1), (position[0] + 1, position[1] - 1),
                                (position[0] + 1, position[1]), (position[0] + 1, position[1] + 1)]
        for need_check_position in need_check_positions:
            if need_check_position[0] < 0 or need_check_position[1] < 0:
                need_check_positions.remove(need_check_position)
                continue
            try:
                if self.board[position[0]][position[1]].is_black() and self.board[need_check_position[0]][
                    need_check_position[1]].is_black():
                    need_check_positions.remove(need_check_position)
            except IndexError:
                pass
            try:
                if self.board[position[0]][position[1]].is_white() and self.board[need_check_position[0]][
                    need_check_position[1]].is_white():
                    need_check_positions.remove(need_check_position)
            except IndexError:
                pass

        for check_position in need_check_positions:
            try:
                if self.board[check_position[0]][check_position[1]] != self.board[position[0]][position[1]]:
                    if self.check_position_for_lose((check_position[0], check_position[1])):
                        self.board[check_position[0]][check_position[1]] = Checker(self, None, (
                            check_position[0], check_position[1]))
            except IndexError:
                pass

    def player_move(self):
        if self.target_position in (self.current_checker.get_available_moves()) and self.board[self.target_position[0]][
                self.target_position[1]].is_empty():
            self.board[self.target_position[0]][self.target_position[1]] = self.current_checker
            self.board[self.current_checker.position[0]][self.current_checker.position[1]] = Checker(self, None, (
                self.current_checker.position[0], self.current_checker.position[1]))
            self.current_checker.position = self.target_position
            self.check_checker_lose((self.target_position[0], self.target_position[1]))
            self.current_checker.check_for_queen_mode_activate()
            self.next_player()
        self.refresh_after_move()

    def check_position_for_lose(self, position):
        try:
            if position[0] != 0:
                if self.board[position[0]][position[1]].is_black():
                    if self.board[position[0] - 1][position[1] + 1].is_white() and \
                            self.board[position[0] + 1][position[1] + 1].is_white():
                        return True
                    if self.board[position[0] + 1][position[1] - 1].is_white() and \
                            self.board[position[0] - 1][position[1] - 1].is_white():
                        return True
                    if self.board[position[0] - 1][position[1] - 1].is_white() and \
                            self.board[position[0] - 1][position[1] + 1].is_white():
                        return True
                    if self.board[position[0] + 1][position[1] - 1].is_white() and \
                            self.board[position[0] + 1][position[1] + 1].is_white():
                        return True
                if self.board[position[0]][position[1]].is_white():
                    if self.board[position[0] - 1][position[1] + 1].is_black() and \
                            self.board[position[0] + 1][position[1] + 1].is_black():
                        return True
                    if self.board[position[0] + 1][position[1] - 1].is_black() and \
                            self.board[position[0] - 1][position[1] - 1].is_black():
                        return True
                    if self.board[position[0] - 1][position[1] - 1].is_black() and \
                            self.board[position[0] - 1][position[1] + 1].is_black():
                        return True
                    if self.board[position[0] + 1][position[1] - 1].is_black() and \
                            self.board[position[0] + 1][position[1] + 1].is_black():
                        return True
        except IndexError:
            pass
        return False

    def closeEvent(self, event):
        self.menu = Menu()
        self.menu.show()
        event.accept()

    def alert(self, message):
        self.msg = QMessageBox()
        self.msg.setText(message)
        self.msg.setWindowTitle("Конец игры")
        self.msg.exec_()
        self.close()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error caught!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QtWidgets.QApplication([])
    application = Menu()
    application.show()
    sys.exit(app.exec())
