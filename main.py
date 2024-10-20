from easyAI import Negamax, Human_Player, AI_Player

from models import Chomp
from ChompGUI import ChompGUI, choose_game_mode

if __name__ == '__main__':
    '''
    ai = Negamax(5)

    if (input("Do you want to play against AI (yes/no | y/n): ").lower()
            in ["yes", "y"]):
        players = [Human_Player(), AI_Player(ai)]
    else:
        players = [Human_Player(), Human_Player()]

    Chomp(players).play()
    '''

    choose_game_mode(15)