import cv2
import mediapipe as mp
import pyautogui

class GestureRecognition:
    def __init__(self):
        """
        Initializes the gesture recognition system, setting up the MediaPipe Hands model.
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.last_thumb_index_distance = 0.0

    def is_thumb_straight(self, hand_landmarks):
        """
        Determines if the thumb is straight based on hand landmarks.

        Args:
            hand_landmarks: A list of hand landmarks for the detected hand.

        Returns:
            bool: True if the thumb is straight, False otherwise.
        """
        thumb_tip = hand_landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks[self.mp_hands.HandLandmark.THUMB_IP]
        thumb_mcp = hand_landmarks[self.mp_hands.HandLandmark.THUMB_MCP]

        # Check if the thumb is in a straight position (either to the left or right)
        return thumb_tip.x < thumb_ip.x < thumb_mcp.x or thumb_tip.x > thumb_ip.x > thumb_mcp.x

    def is_index_finger_straight(self, hand_landmarks):
        """
        Determines if the index finger is straight based on hand landmarks.

        Args:
            hand_landmarks: A list of hand landmarks for the detected hand.

        Returns:
            bool: True if the index finger is straight, False otherwise.
        """
        # Extract landmarks for the index finger
        index_tip = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_dip = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP]
        index_pip = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        index_mcp = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]

        # Check if the y-coordinates of the index finger landmarks decrease monotonically
        return index_tip.y < index_dip.y < index_pip.y < index_mcp.y

    def is_fist(self, hand_landmarks):
        """
        Determines if the hand is in a fist shape (excluding the thumb).

        Args:
            hand_landmarks: A list of hand landmarks for the detected hand.

        Returns:
            bool: True if the hand is in a fist shape, False otherwise.
        """
        # Extract landmarks for the fingers and palm
        thumb_tip = hand_landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks[self.mp_hands.HandLandmark.PINKY_TIP]
        palm_base = hand_landmarks[self.mp_hands.HandLandmark.WRIST]

        # Define a limit to check if fingers are closed
        limit = 0.2
        if abs(thumb_tip.y - palm_base.y) > limit and abs(index_tip.y - palm_base.y) > limit and \
                abs(middle_tip.y - palm_base.y) < limit and abs(ring_tip.y - palm_base.y) < limit and \
                abs(pinky_tip.y - palm_base.y) < limit:
            return True
        return False

    def recognize_gesture(self, hand_landmarks):
        """
        Recognizes specific gestures based on the hand landmarks.

        Args:
            hand_landmarks: A list of hand landmarks for the detected hand.

        Returns:
            str: A string indicating the recognized gesture (e.g., "Skip Left", "Increase volume").
        """
        if not hand_landmarks:
            return "No hand detected"

        # Extract thumb and index tip landmarks for gesture recognition
        thumb_tip = hand_landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_index_distance = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)

        # Recognize swipe gestures based on the index finger's position
        if self.is_index_finger_straight(hand_landmarks) and not self.is_thumb_straight(hand_landmarks):
            index_tip_x = index_tip.x
            index_dip_x = hand_landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_DIP].x

            # Determine left or right swipe based on x-coordinate comparison
            if index_tip_x < index_dip_x:
                pyautogui.press("left")
                return "Skip Left"
            elif index_tip_x > index_dip_x:
                pyautogui.press("right")
                return "Skip Right"

        # Adjust volume based on the change in thumb-index distance
        elif self.last_thumb_index_distance != 0.0 and self.is_thumb_straight(hand_landmarks):
            if thumb_index_distance > self.last_thumb_index_distance:
                pyautogui.press("volumeup")
                return "Increase volume"
            elif thumb_index_distance < self.last_thumb_index_distance:
                pyautogui.press("volumedown")
                return "Decrease volume"

        self.last_thumb_index_distance = thumb_index_distance
        return "Gesture not recognized | PAUZE"

    def process_frame(self, frame, hands):
        """
        Processes a single video frame to detect hand gestures.

        Args:
            frame: The current video frame.
            hands: The MediaPipe Hands object used to process the frame.

        Returns:
            frame: The processed frame with gesture information drawn on it.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # If hand landmarks are detected, process the gestures
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture = self.recognize_gesture(hand_landmarks.landmark)
                # Display recognized gesture on the frame
                cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

        return frame

    def run(self):
        """
        Starts the webcam feed and continuously processes frames for gesture recognition.

        Captures frames from the webcam, processes them to detect hand gestures,
        and performs corresponding actions (e.g., controlling volume, skipping).
        """
        cap = cv2.VideoCapture(0)

        # Use MediaPipe Hands model with optimized parameters
        with self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7
        ) as hands:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame from camera.")
                    break

                frame = cv2.flip(frame, 1)  # Flip frame for mirror effect
                frame = self.process_frame(frame, hands)
                cv2.imshow('Gesture Recognition', frame)

                # Press 'q' to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_recognition = GestureRecognition()
    gesture_recognition.run()
