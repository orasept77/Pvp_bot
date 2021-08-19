from exceptions import *
from player import Player
import random

class Game:
    tokens = ('X', 'O')

    def __init__(self, board_size=3):
        self.board_size = board_size
        self.empty_space = '-'
        self.board = [[self.empty_space] * board_size for i in range(board_size)]
        self.started = False
        self.players = {}
        self.current_player = None

    def getBoard(self):
        return self.board

    def getBoardString(self):
        board_string = []
        for row in self.board:
            board_string.append(' , '.join((str(x) for x in row)))

        return '\n'.join((str(x) for x in board_string))

    def getPlayers(self):
        players = '\n'.join((self.players[x].name + ' - ' + self.players[x].token for x in self.players))
        return players

    def move(self, pos, player_id):
        if player_id not in self.players:
            raise NotInGameError()
        if not self.started:
            raise GameNotStartedError()
        if not player_id == self.current_player:
            raise InvalidMoveError()
        player = self.players[player_id]
        token = player.token
        if pos < 1 or pos > self.board_size ** 2:
            raise InvalidMoveError()
        row = (pos - 1) // self.board_size
        col = (pos - 1) % self.board_size
        if self.board[row][col] == self.empty_space:
            self.board[row][col] = token
        else:
            raise InvalidMoveError()

    def next(self):
        for player_id in self.players:
            if player_id != self.current_player:
                self.current_player = player_id
                return

    def add_player(self, player_id, name):
        global token
        if len(self.players) >= 2:
            raise PlayerLimitError()
        if player_id in self.players:
            raise AlreadyJoinedError()
        if len(self.players) == 0:
            token = random.choice(self.tokens)
        else:
            for p in self.players:
                if self.players[p].token == self.tokens[0]:
                    token = self.tokens[1]
                else:
                    token = self.tokens[0]

        self.players[player_id] = Player(player_id, name, token)
        return token

    def remove_player(self, player_id):
        if self.started:
            raise GameStartedError()
        if player_id in self.players:
            del self.players[player_id]
        else:
            raise NotInGameError()

    def start(self):
        if self.started:
            raise GameStartedError()
        elif len(self.players) < 2:
            raise TooFewPlayersError()
        self.current_player = random.choice(list(self.players.keys()))
        self.started = True

    def checkWin(self, player_id):
        if player_id not in self.players:
            return
        player = self.players[player_id]
        token = player.token
        for row in self.board:
            if all((x == token for x in row)):
                return True

        for i in range(0, self.board_size - 1):
            if all((self.board[j][i] == token for j in range(0, self.board_size))):
                return True

        if all((self.board[i][i] == token for i in range(0, self.board_size))):
            return True
        if all((self.board[self.board_size - 1 - i][i] == token for i in range(0, self.board_size))):
            return True
        return False