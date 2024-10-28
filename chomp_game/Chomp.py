from easyAI import TwoPlayerGame, Player

class Chomp(TwoPlayerGame):
    def __init__(self,players: list[Player] = None, max_x: int = 5, max_y: int = 5):
        self.players: list[Player] = players
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.board: list[list[int]] = [[1 for _ in range(self.max_x)] for _ in range(self.max_y)]
        self.current_player: int = 1

    def possible_moves(self) -> list[str]:
        """
        function required by easyAI, lists possible moves.
        forwards list of strings e.g. '11' which represents 'xy' coordinates

        Returns:
        list[str]:Returning value
        """
        moves = ["11"]
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.board[y][x] == 1 and not (x == 0 and y == 0):
                    moves.append(f"{x + 1}{y + 1}")
        return moves

    def make_move(self, move: str):
        """
        Cuts the board based on field coordinates.

        Parameters:
        move (str): A string representing a move, where the string is made up of two digits, e.g., '11'.
        The string is split into two parts: the first digit represents the x-coordinate, and the second digit
        represents the y-coordinate of the move on a grid or board.
        """
        x = int(move[0]) - 1
        y = int(move[1]) - 1

        if self.board[y][x] == 1:  # Check if the field is available
            # Cut the board
            for i in range(y, self.max_y):
                for j in range(x, self.max_x):
                    self.board[i][j] = 0

    def win(self) -> bool:
        """
        function required by easyAI, determines whether a player wins

        Returns:
        bool:Returning value
        """
        return self.board[0][0] == 0

    def is_over(self) -> bool:
        """
        function required by easyAI, returns win() function result

        Returns:
        bool:Returning value
        """
        return self.win()

    def show(self):
        """
        function that display a board in terminal.
        """
        for row in self.board:
            print(row)
        print()
        if self.win():
            print(f"Player {2 if self.current_player == 1 else 1} wins!")

    def scoring(self) -> int:
        """
        function required by easyAI, determines when to reward ai for his move

        Returns:
        int:Returning value
        """
        return 100 if self.win() else 0