# Authors 
Jakub Pobłocki |  Kacper Pecka

# Automated Anti-Aircraft Defense System

## Description
The Automated Anti-Aircraft Defense System leverages **fuzzy logic** to assess and respond to airborne threats. The system is structured into three modules that work closely together to ensure a swift, accurate, and efficient response to incoming threats.

## Modules

### 1. Threat Assessment Module
This module calculates the threat level posed by an object, considering:
- **Distance** between the missile launcher and the target
- **Movement status** of the object (whether it is in motion)
- **Armament status** of the object (whether it is armed)

These parameters allow the system to assess the potential threat and pass this information to the next module for a decision on engagement.

### 2. Engagement Decision Module
Based on the assessed threat level, as well as the speed and trajectory of the incoming object, this module determines whether a missile should be deployed. The decision-making process ensures countermeasures are only deployed when necessary, optimizing resource usage.

### 3. Missile Selection Module - **Under Development**
This module will be responsible for selecting the most appropriate missile type to neutralize the threat. The missile selection is based on the following parameters:
- **Target distance**: Missiles with a shorter range are selected for closer targets.
- **Target speed**: Faster targets require faster missiles.
- **Target trajectory**: Maneuvering targets may require missiles with better guidance capabilities.
- **Threat level**: Higher threat levels result in the selection of more precise missiles.

The missile selection is managed using fuzzy logic to ensure flexibility and accuracy in countermeasure deployment.

## User Interface

The user interface (UI) of the **Automated Anti-Aircraft Defense System** is designed to be intuitive and easy to use, providing clear controls and real-time information about the system’s operations. The interface consists of several key components that allow users to configure, visualize, and interact with the defense system.

### 1. **Control Panel**
The control panel is the main part of the UI, located on the right side of the screen. It is where users can set parameters, interact with the system, and monitor the status of the UFOs.

#### Key Features of the Control Panel:
- **Sliders**: The control panel includes sliders that allow users to adjust the following parameters:
  - **Altitude**: Adjusts the altitude of the UFO, affecting its vertical position on the screen.
  - **Speed**: Controls the speed of the UFO, affecting how fast it moves across the screen.
  - **Weapon**: Toggles the weapon status of the UFO (0 for no weapon, 1 for armed).

- **"GO!" Button**: This button is used to generate a new UFO based on the current values set by the sliders (altitude, speed, and weapon). Once pressed, the UFO is created and starts moving across the screen.

- **Altitude Scale**: A vertical scale on the left side of the control panel shows the altitude range, helping users visualize the altitude in relation to the sliders' settings.

### 2. **UFO Display Area**
On the left side of the screen, the UFOs are displayed as moving objects. The UFO's appearance, including its speed and altitude, is dynamically updated as the sliders are adjusted. The UFOs move horizontally across the screen, and their vertical position corresponds to the altitude set using the slider.

- **Hovering over a UFO**: When the user moves the mouse over a UFO, its details (altitude, speed, and weapon status) are displayed in the control panel, providing real-time feedback on the selected UFO.

### 3. **Detailed Information for Selected UFO**
When the user hovers over a UFO, its details are shown in the control panel:
- **Altitude**: Displays the current altitude of the UFO.
- **Speed**: Shows the current speed of the UFO in kilometers per hour.
- **Weapon**: Indicates whether the UFO is armed (0 for unarmed, 1 for armed).

Additionally, an image of the UFO is shown on the screen, allowing users to visually track the object's position.

### 4. **Graphics and Visuals**
The system uses **pygame** for rendering all visual components, including UFOs, sliders, buttons, and scale. The UFO is represented as an image and moves across the screen based on its speed and altitude.

The interface is designed to be responsive and intuitive, allowing users to interact with the system and monitor the defense system's performance in real-time.

### 5. **Radar Detection and Threat Visualization**
The system includes an enhanced radar module that detects UFOs within a specified range and visually highlights them.

#### Key Features:
- **Detection Rectangle**: When a UFO is within the radar range, a **red rectangle** is drawn around it, indicating that the system has detected the object.
- **Threat Level Bar**: A bar below the detected UFO displays the current threat level, dynamically updated based on the UFO's speed, altitude, and armament status.
- **LED Indicator**: The LED indicator next to the UFO's details changes color based on the decision made by the **Engagement Decision Module** (the second module in the system). If the module assesses the UFO as a high threat and determines that it should be engaged, the LED indicator will turn **red**. If the threat level is low, the indicator will remain **green**.

These visual cues help the operator quickly assess the threat and take appropriate action, enabling efficient response during critical moments.

## An example of what the simulation looks like
[Watch the demo video](https://youtu.be/cHLMgfb8OpE)

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
Before running the command, navigate to the `Z2_SELF_GUIDED_MISSILE` directory.

```bash
pip install -r requirements.txt
```


## Cloning the Repository
To get started with the Automated Anti-Aircraft Defense System, you need to clone the repository. Use the following command in your terminal:

```git clone https://github.com/s25770-pj/NAI_CHOMP.git```

### Running the Game
1. **Open a Terminal**:
   - Navigate to the directory where you cloned the repository.
   - Go to Z2_SELF_GUIDED_MISSILE dictionary.

2. **Run the Game**:
   - Use the command `python main.py` to start the game.

