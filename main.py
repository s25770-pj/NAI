from easyAI import Negamax, Human_Player, AI_Player

from models import Chomp

if __name__ == '__main__':
    ai = Negamax(50)
    game = Chomp([Human_Player(), AI_Player(ai)])
    history = game.play()
