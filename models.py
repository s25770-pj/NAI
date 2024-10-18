from easyAI import TwoPlayerGame


class Chomp(TwoPlayerGame):
    def __init__(self, players=None):
        """
        Board initialization
        """
        self.players = players
        self.max_x = 5
        self.max_y = 5
        self.board = [[1 for _ in range(self.max_x)] for _ in range(self.max_y)]
        self.current_player = 1

    def possible_moves(self):
        moves = []
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.board[y][x] == 1 and not (x == 0 and y == 0):
                    moves.append(f"{x + 1}{y + 1}")  # Store as string with 1-based index

        moves.append("11")
        return moves

    def make_move(self, move):
        """
        Cuts the board based on field coordinates.
        """
        x = int(move[0]) - 1
        y = int(move[1]) - 1

        if self.board[y][x] == 1:  # Check if the field is available
            # Cut the board
            for i in range(y, self.max_y):
                for j in range(x, self.max_x):
                    self.board[i][j] = 0

    def win(self):
        return self.board[0][0] == 0

    def is_over(self):
        return self.win()

    def show(self):
        """
        Displays board.
        """
        for row in self.board:
            print(row)
        print()

    def scoring(self):
        return 100 if self.win() else 0
