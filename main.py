from models import Chomp


if __name__ == '__main__':
    while True:
        board_size = input("Write size of the board: ").split(',')

        x, y = board_size[:2] if all(value.strip().isdigit() for value in board_size) else (5, 5)

        game = Chomp([int(x), int(y)])
        game.display_board()

        while not game.game_over:
            print(f"Player{game.player} turn")
            field = input("Which field to cut: ").split(',')

            if all(value.strip().isdigit() for value in field):
                x, y = field[:2]
                game.cut([int(x), int(y)])
            else:
                print("Provided values are not correct integers")

        restart = input("Do you want to play again? (yes/no): ").lower()

        if restart != 'yes':
            print("Thanks for playing!")
            break