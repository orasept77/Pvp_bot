class TicTacToeError(Exception):
    pass


class PlayerLimitError(TicTacToeError):
    pass


class AlreadyJoinedError(TicTacToeError):
    pass


class NotInGameError(TicTacToeError):
    pass


class GameStartedError(TicTacToeError):
    pass


class TooFewPlayersError(TicTacToeError):
    pass


class InvalidMoveError(TicTacToeError):
    pass


class GameNotStartedError(TicTacToeError):
    pass