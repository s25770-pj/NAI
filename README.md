<<<<<<< HEAD
# NAI_CHOMP
Chomp game againt AI 
=======
# Authors 
Jakub Pobłocki 
Kacper Pecka

# Rules of Chomp

## Objective
The goal of the game is to force your opponent to eat the last "square" (element) on the board.

## Setup
1. **Board**: The game is played on a rectangular board made up of squares, resembling a chocolate bar. A typical size is 5x5, but different sizes can be used.
2. **Gameplay Rules**: Each square on the board can be eaten, and when a square is eaten, all squares to the right and below that square are also removed.

## Gameplay
1. **Moves**: Players take turns making moves. On their turn, a player chooses a square to eat.
2. **Eating Rules**: When a square (e.g., at position x, y) is eaten, all squares in the same row to the right (including the chosen square) and in the same column below (including the chosen square) are also removed from the board.
3. **End of Game**: The game ends when one player cannot make a move, which means they had to eat the last square. That player loses.

## Example Move
If there is a 4x4 board and a player chooses the square at position (2, 2), they will eat all squares in columns 2 and 3 and in rows 2 and 3.

## Strategy
- Pay attention to the moves you leave for your opponent.
- Try to force your opponent into a position where they have to eat the last square.

# Setting Up the Chomp Game in Python

## Prerequisites
- Ensure that Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

## Running the Game

1. **Clone the repository**
   - Clone the repository from github using command: git clone ```https://github.com/s25770-pj/NAI_CHOMP.git```

2. **Open a Terminal**:
   - Open dictionary in environment that handles python3.
   - Navigate to the directory where your `main.py` file is located.

4. **Run the Game**:
   - Use the command `python main.py` to start the game.

Enjoy playing Chomp!
>>>>>>> origin/master
