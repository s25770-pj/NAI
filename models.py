from easyAI import TwoPlayerGame, Negamax, Human_Player, AI_Player

class Chomp(TwoPlayerGame):
    def __init__(self, players=None):
        """
        Board initialization
        """
        self.players = players
        self.x = 5
        self.y = 5
        self.board = [[1 for _ in range(self.x)] for _ in range(self.y)]
        self.current_player = 1

    def possible_moves(self):
        moves = []
        for y in range(self.y):
            for x in range(self.x):
                if self.board[y][x] == 1:
                    moves.append(f"{x + 1}{y + 1}")  # Store as string with 1-based index
        print(f'moves: {moves}')
        return moves

    def make_move(self, move):
        """
        Cuts the board based on field coordinates.
        """
        x = int(move[0]) - 1
        y = int(move[1]) - 1
        print(f'x: {x}, y: {y}')

        if self.board[y][x] == 1:  # Check if the field is available
            # Cut the board
            for i in range(y, self.y):
                for j in range(x, self.x):
                    self.board[i][j] = 0

    def win(self):
        return len(self.possible_moves()) == 1

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

