# Authors  
Jakub Pobłocki | Kacper Pecka

# ✋ Gesture Recognition System with MediaPipe and OpenCV

This project is a gesture recognition system using **MediaPipe** and **OpenCV**, designed for controlling multimedia through real-time hand gestures. The system interprets hand gestures, such as thumb or index finger movements, to perform actions like video navigation or volume control.

## How It Works 🚀
- **Hand Detection** – The system uses MediaPipe's hand module to detect and track hand landmarks based on webcam input.
- **Gesture Recognition** – The system interprets gestures based on hand landmarks:
  - **Video Navigation**:
    - If the **index finger is straight**, while **all other fingers are bent**, the system interprets the direction of the index finger:
      - **Left** – Skip backward.
      - **Right** – Skip forward.
  - **Volume Control**:
    - If **all fingers are bent except the thumb**, the system measures the distance between the thumb and the index finger:
      - **Increasing distance** – Volume up.
      - **Decreasing distance** – Volume down.
  - **No Interaction**:
    - If no gesture is recognized, the system performs no action and remains in a "pause" state.

## User Interface in OpenCV 🎮

The system runs with a webcam-based interface:

1. **Camera Feed** – The main window displays the live video feed from the webcam.
2. **Gesture Display** – The recognized gesture is displayed in real-time (e.g., "Skip Left", "Increase Volume").
3. **Interaction** – The system performs the corresponding action based on the recognized gesture.

## Optimized Functionality

The system operates within the OpenCV environment, providing the following features:

- **Real-Time Gesture Recognition** – Continuously analyzes the webcam feed, recognizing gestures, and responding instantly.
- **Video Navigation** – Based on the direction of the index finger.
- **Volume Control** – Adjusts the volume based on the changing distance between the thumb and index finger.
- **Pause State** – No action when no gesture is detected.

## Example of the System in Action
[Watch the demo](https://youtu.be/9PAuXugydck)

## Prerequisites
- Python (recommended version 3.7 or later). Download it from [python.org](https://www.python.org/downloads/).
- A webcam for real-time hand gesture detection.

### Installing Dependencies
Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

This will install dependencies such as `opencv-python`, `mediapipe`, and `pyautogui`.

## Cloning the Repository
To get started with the gesture recognition system, clone the repository using the following command:

```bash
git clone https://github.com/s25770-pj/NAI.git
```

### Running the Program
1. **Open a Terminal**:
   - Navigate to the directory where you cloned the repository.
   - Enter the project folder:
   
```bash
cd Z6
```

2. **Run the Program**:
   - Use the command `python main.py` to start the gesture recognition system.

## Troubleshooting
- If installing `mediapipe` fails, ensure you are using a compatible Python version (recommended 3.7+).
- Verify that your webcam is working properly and is accessible to OpenCV.
