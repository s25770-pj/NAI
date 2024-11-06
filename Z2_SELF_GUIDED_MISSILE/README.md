# Authors 
Jakub Pobłocki |  Kacper Pecka
# Automatic Anti-Aircraft System

The system, as its name suggests, is an automated anti-aircraft defense mechanism that leverages fuzzy logic to assess and respond to airborne threats. It is structured into three distinct computational modules:

1. Threat Assessment Module: This initial module calculates the threat level posed by an object, factoring in the current distance between the missile launcher and the target, the object’s movement status, and whether it is armed. These inputs collectively enable the system to gauge the potential threat that the object represents.

2. Engagement Decision Module: Based on the assessed threat level, as well as the speed and trajectory of the incoming object, this module determines the need for missile deployment. This decision-making process ensures that countermeasures are only deployed when necessary, optimizing resource usage.

3. Missile Selection Module: For confirmed engagements, this final module identifies the most suitable missile type to neutralize the threat. This selection process is based on the target’s distance, speed, and trajectory, ensuring that the countermeasure is effectively matched to the threat profile.

Each module operates in a sequence to ensure that the system provides a swift, accurate, and efficient response to airborne threats.

## Example Gameplay

Below are examples of gameplay, showing system operation.

| START | Move 1 | Move 2 | Move 3 | Move 4 |
|--------|--------|--------|--------|--------|
| <div style="text-align: center;display:flex;justify-content: space-around;"><img src="image/start_game.png" alt="Play 1" width="150" height="150"/><img src="image/play_1.png" alt="Play 1" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_2.png" alt="Play 2" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_3.png" alt="Play 3" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_3_1.png" alt="Play 4" width="150" height="150"/></div> | <div style="text-align: center;"><img src="image/play_4.png" alt="Play 5" width="150" height="150"/></div> |
| *This is what the board looks like at the start; the human player always goes first.* | *The player makes a move by choosing (4,3).* | *AI responds with a move (2,2).* | *The player makes a strategic move (5,1).* | *AI makes a move (1,5).* |

# Setting Up the Tracking Flying Objects Game/Simulation in Python

## Prerequisites
- Ensure that Python is installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

## Required Libraries
Make sure you have the following libraries installed:

- `networkx`
- `noise`
- `numpy`
- `pydantic`
- `pydantic-settings`
- `pygame`
- `scikit-fuzzy`
- `scipy`


You can install the required libraries using the command:
Before you use the command, navigate to Z2_SELF_GUIDED_MISSILE dictionary.

```bash
pip install -r requirements.txt
```


## Cloning the Repository
To get started with the Chomp game, you need to clone the repository. Use the following command in your terminal:
```git clone https://github.com/s25770-pj/NAI_CHOMP.git```

### Running the Game
1. **Open a Terminal**:
   - Navigate to the directory where you cloned the repository.
   - Go to Z2_SELF_GUIDED_MISSILE dictionary.

2. **Run the Game**:
   - Use the command `python main.py` to start the game.

Enjoy playing Chomp!
