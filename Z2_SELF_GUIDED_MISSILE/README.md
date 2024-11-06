# Authors 
Jakub Pobłocki |  Kacper Pecka
# Chomp Game

Chomp is a two-player game played on a rectangular grid of squares, where players take turns eating squares. The objective is to force your opponent to eat the last square, leading to their loss. This project implements the Chomp game using Python and the EasyAI library for AI opponents.

# Rules of Chomp

## Objective
The goal of the game is to force your opponent to eat the last "square" (element) on the board.

## Setup
1. **Board**: The game is played on a rectangular board made up of squares, resembling a chocolate bar. A typical size is 5x5, but different sizes can be used ranging from 2x2 to 5x5.
2. **Gameplay Rules**: Each square on the board can be eaten, and when a square is eaten, all squares to the right and below that square are also removed.

## Gameplay
1. **Moves**: Players take turns making moves. On their turn, a player chooses a square to eat.
2. **Eating Rules**: When a square (e.g., at position x, y) is eaten, all squares in the same row to the right (including the chosen square) and in the same column below (including the chosen square) are also removed from the board.
3. **End of Game**: The game ends when one player cannot make a move, which means they had to eat the last square. That player loses.

## Example Move
If there is a board size ranging from 2x2 to 5x5, and a player chooses the square at position (2, 2), they will eat all squares to the right and down from this block.

## Example Gameplay

Below are examples of gameplay in Chomp, showing consecutive moves.

| START | Move 1 | Move 2 | Move 3 | Move 4 |
|--------|--------|--------|--------|--------|
| <div style="text-align: center;display:flex;justify-content: space-around;"><img src="image/start_game.png" alt="Play 1" width="150" height="150"/><img src="image/play_1.png" alt="Play 1" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_2.png" alt="Play 2" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_3.png" alt="Play 3" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_3_1.png" alt="Play 4" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_4.png" alt="Play 5" width="150" height="150"/></div> |
| *This is what the board looks like at the start; the human player always goes first.* | *The player makes a move by choosing (4,3).* | *AI responds with a move (2,2).* | *The player makes a strategic move (5,1).* | *AI makes a move (1,5).* |

| Move 5 | Move 6 | Move 7 | Move 8 | Move 9 |
|--------|--------|--------|--------|--------|
| <div style="text-align: center;"><img src="image/play_5.png" alt="Play 6" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_6.png" alt="Play 7" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_7.png" alt="Play 8" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_8.png" alt="Play 9" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_9.png" alt="Play 10" width="150" height="150"/></div> |
| *The player makes a move (1,3).* | *AI responds with a move (3,1).* | *The player plays (2,1).* | *AI makes a move (1,2).* | *The player moves to (1,1), resulting in a loss.* |

## Strategy
- Pay attention to the moves you leave for your opponent.
- Try to force your opponent into a position where they have to eat the last square.

# Setting Up the Chomp Game in Python

## Prerequisites
- Ensure that Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

## Required Libraries
Make sure you have the following libraries installed:

- `easyAI`
- `tkinter` (this is usually included with Python)

You can install the required libraries using the command:

```bash
pip install easyAI
```

## Cloning the Repository
To get started with the Chomp game, you need to clone the repository. Use the following command in your terminal:
```git clone https://github.com/s25770-pj/NAI_CHOMP.git```

### Running the Game
1. **Open a Terminal**:
   - Navigate to the directory where you cloned the repository.

2. **Run the Game**:
   - Use the command `python main.py` to start the game.

Enjoy playing Chomp!
