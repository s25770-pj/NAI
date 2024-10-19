from easyAI import Negamax, Human_Player, AI_Player

from models import Chomp

if __name__ == '__main__':
    ai = Negamax(13)

    if (input("Do you want to play against AI (yes/no | y/n): ").lower()
            in ["yes", "y"]):
        players = [Human_Player(), AI_Player(ai)]
    else:
        players = [Human_Player(), Human_Player()]

    Chomp(players).play()
