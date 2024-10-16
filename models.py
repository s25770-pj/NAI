class Chomp(object):
    def __init__(self, board_size: list[int]):
        """
        Board initialization
        """
        self.size = board_size
        self.board = [[1 for _ in range(board_size[0])] for _ in range(board_size[1])]
        self.player = 1
        self.game_over = False

    def display_board(self):
        """
        Displays board
        """
        for row in self.board:
            print(row)
        print()

    def cut(self, field: list[int]):
        """
        Cuts the board basing on field coordinates

        :param field: list of integers representing coordinates of the field to cut
        :return: integer representing actual player
        """
        try:
            selected_field = self.board[field[1]-1][field[0]-1]

            # check if selected field is not already cut out
            if selected_field == 0:
                pass
            else:
                self.board[field[1]-1][field[0]-1] = 0

                # cuts (changes 1's to 0's) in appropriate fields
                for y in range(field[1]-1, len(self.board)):
                    for x in range(field[0]-1, len(self.board[y])):
                        self.board[y][x] = 0

                self.display_board()

                # check if player cut death field
                if field[0] == 1 and field[1] == 1:
                    print(f'player {2 if self.player == 1 else 1} won')
                    self.game_over = True

                # change for the next player after cut
                self.player = 1 if self.player == 2 else 2
        except IndexError:
            print(f'Incorrect index provided')
