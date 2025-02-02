# **Face and Gesture Recognition System**

This project utilizes facial recognition and hand gesture detection to monitor and classify individuals, allowing access or denying based on predefined conditions. It integrates emotion detection and gesture recognition functionalities in real-time through a video feed.


## Requirements

To install all necessary dependencies, run:
```bash	
	pip install -r requirements.txt
```
The requirements file include the following libraries:
- OpenCV (cv2): For image and video processing
- face_recognition: For face recognition
- FER: For emotion recognition
- mediapipe: For hand gesture detection
- numpy: For numerical operations
- uuid, random, and platform: For unique identifiers and OS detection
- time: For managing time-related functions


## Overview

The program captures a video feed, detecting faces and performing the following:
1. ace Recognition: Identifies known faces from whitelisted and blacklisted directories, categorizing individuals as "allowed" or "banned".
2. Emotion Detection: Analyzes emotions based on the face using FER (Facial Expression Recognition).
3. Hand Gesture Recognition: Detects specific hand gestures (like "OK" or "Not OK") through mediapipe.
4. Stranger Detection: Any unrecognized faces are stored in a "stranger" folder for later review.


## Directories

- Whitelist: Contains images of individuals who are allowed access.
- Blacklist: Contains images of individuals who are denied access.
- Strangers: Stores images of unrecognized faces.


## Functions

1. get_centered_text_coordinates: Calculates coordinates to center text on the screen.
2. imgs_encodings_loader: Loads images and encodings for known individuals.
3. detect_hand_gesture: Detects specific hand gestures ("OK", "Not OK", or "No detected").
4. main: The core loop for video capture, face recognition, and emotion detection.


## Usage

1. Ensure your camera is connected.
2. Place known faces in the whitelist and blacklist directories (ensure the images are well-lit and clear).
3. Run the program:
```bash	
	python your_script.py
```
The program will start capturing video and display detected faces, emotions, and hand gestures, as well as allowing or denying access based on the recognition results.


## Notes

- You can press Esc to stop the video feed.
- The program currently only works on Linux and Windows operating systems.


# Additional Features and Details

## Emotion detection with FER

- The FER library is used to analyze the emotions of detected faces.
- It detects various emotions like happiness, sadness, surprise, anger, etc.
- The program will display the predominant emotion detected in real-time on the video feed.


## Hand gesture recognition

The hand gestures, specifically "OK" and "Not OK", are detected using mediapipe, which is a framework by Google for real-time hand tracking. The system tracks key points of the hand and classifies the gesture based on the position of the fingers.


## Gesture Recognition Process:

- The program checks if all fingers are bent (indicating a fist) and if the thumb is above or below the wrist to identify "OK" or "Not OK".
- The gesture is shown on the screen in real-time.


## Stranger detection

- Any unrecognized face will be saved into the strangers directory.
- A random name (based on UUID) is assigned to the new stranger, and their face is stored as an image file.
- This feature allows the system to build a database of unknown faces for future recognition or review.


## Access Control Logic

- The system checks if the detected face is in the whitelist or blacklist
- If the face is in the whitelist, the program grants access and labels the person as "allowed."
- If the face is in the blacklist, it denies access and labels the person as "banned."
- If the face is not recognized, the system checks the stranger database and, if new, stores their image.


# System requirements

- Python 3.x: Ensure you are using Python 3.6 or higher.
- OpenCV: Version 4.0 or above.
- mediapipe: Version 0.8.6 or above (for hand gesture detection).
- face_recognition: Version 1.3.0 or above.




# License
This project is open-source and can be freely used, modified, and distributed. However, make sure to adhere to any respective licenses of the libraries used (such as FER, mediapipe, etc.).






