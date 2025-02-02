# To install libraries use pip install -r requirements.txt

# Imports
import cv2                              # image and video process and web management
import face_recognition as fr           # face recognition library
import os                               
import numpy                            
from datetime import datetime   
import platform  
from fer import FER
import uuid
import random
import time
import mediapipe as mp

# functions
def get_centered_text_coordinates(rect_top_left, rect_bottom_right, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.7, thickness=2):
    """
    calc coords to get coords to center text

    :param rect_top_left: coord x1,y1 from rectangle.
    :param rect_bottom_right: coord x2,y2 from rectangle.

    :param text: texto.
    :param font: text font.

    :param font_scale: font scale.
    :param thickness: text thickness.
    :return: text coords.
    """
    
    # get text font size
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # rectangle coords
    rect_x1, rect_y1 = rect_top_left
    rect_x2, rect_y2 = rect_bottom_right

    # calc text coords
    center_x = (rect_x2 + rect_x1 - text_width) // 2
    center_y = (rect_y2 + rect_y1 + text_height) // 2

    return (center_x, center_y)


def imgs_encodings_loader(folder_path):
    images = []
    names = []
    encodings = []
    for file_name in os.listdir(folder_path):
        image = cv2.imread(f"{folder_path}/{file_name}")
        image = cv2.flip(image, 1)
        name = os.path.splitext(file_name)[0]
        face_loc = fr.face_locations(image)
        if face_loc:
            encoding = fr.face_encodings(image, known_face_locations=[face_loc[0]])[0]
            images.append(image)
            names.append(name)
            encodings.append(encoding)
        else:
            print(f"No se detectaron rostros en {file_name}.")
    return images, names, encodings

def detect_hand_gesture(frame, hands, mp_hands, mp_drawing):
    '''
    function to detect specific hand gestures: 'Ok' and 'Not ok'

    Args: frame as actual frame

    Returns: hand gesture detected: 'Ok', 'Not ok', 'No detected'
    '''

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    gesture = 'No detected'

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Obtener las coordenadas de los puntos clave necesarios
            # Índices de los landmarks según MediaPipe:
            # 4: Pulgar (Tip)
            # 3: Pulgar (IP)
            # 2: Pulgar (MCP)
            # 1: Pulgar (CMC)
            # 0: Muñeca
            # 9: Dedo Medio (MCP)
            # Detección de puño: dedos (índice, medio, anular y meñique) doblados

            bent_fingers = 0

            for finger_id in [8,12,16,20]:
                    finger_tip_y = hand_landmarks.landmark[finger_id].y
                    finger_mcp_y = hand_landmarks.landmark[finger_id - 2].y

                    if finger_tip_y > finger_mcp_y:
                        bent_fingers += 1

            fist = bent_fingers == 4        # if 4 fingers are bent, we have a fist

            # get thumb position
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
            thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
            thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]

            # get wrist position
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # check thumb position
            if fist:
                # to check if thumb is up, the thumb tip is less than wrist
                if thumb_tip.y < wrist.y:       
                    gesture = "OK" 
                    print(thumb_tip.y)          
                    print(wrist.y)              
                    

                elif thumb_tip.y > wrist.y:     
                    gesture = "No OK"
                    print(thumb_tip.y)          
                    print(wrist.y)              
                    

            # draw hand notation in frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    return gesture


#########################################################################################


#start program
def main():

    # databases
    whitelist_path = './whitelist'
    blacklist_path = './blacklist'
    strangers_path = './strangers'

    # dir checker
    os.makedirs(whitelist_path, exist_ok=True)
    os.makedirs(blacklist_path, exist_ok=True)
    os.makedirs(strangers_path, exist_ok=True)

    # load the imgs and encodings using a function
    allowedImgs, allowedNames, allowedFaceEncondings = imgs_encodings_loader(whitelist_path)
    bannedImgs, bannedNames, bannedFaceEncondings = imgs_encodings_loader(blacklist_path)
    strangerImgs, strangerNames, strangersFaceEncodings = imgs_encodings_loader(strangers_path)

    # check feelings with fer
    emotion_detector = FER()            # fer instance

    # camera setup deppending the OS
    video = None
    if platform.system() == 'Linux':
        video = cv2.VideoCapture(0)                     # Default behavior for Linux
    elif platform.system() == 'Windows':
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)      # Default behavior for Windows
    else:
        raise Exception("Unsupported operating system")    


    # hand detection
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)


    try:
        # loop to process the video
        while True:
            ret, frame = video.read()   # read the frame from video

            if not ret:            # if the first frame is not available, break the loop
                break

            face_locations = fr.face_locations(frame)   # detect the faces and their paths

            # get how much faces are in front camera
            n_faces = f'{len(face_locations)} caras detectadas'
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (255, 255, 255)  
            thickness = 2
            
            # get the frame h and w
            height, width = frame.shape[:2]

            # show text
            cv2.putText(frame, n_faces, (10, 30), font, font_scale, color, thickness)

            # check if the face could be recognized
            if face_locations != []:
                face_frame_encodings = fr.face_encodings(frame, known_face_locations=face_locations)    # Encode the face

                # for every frame
                for face_frame_encoding, face_locations in zip(face_frame_encodings, face_locations):

                    name = 'Unknown'
                    color = (0, 0, 255)         # red for unknowns 
                    entryAllowed = 'Paso restringido'
                    
                    # check white list
                    if allowedFaceEncondings:
                        result = fr.compare_faces(allowedFaceEncondings, face_frame_encoding)
                        distances = fr.face_distance(allowedFaceEncondings, face_frame_encoding)
                        
                        if any(result):  # check result
                            bestMatch = numpy.argmin(distances)
                            if result[bestMatch]:
                                name = f'{allowedNames[bestMatch]}'
                                color = (0, 255, 0)  # set color to green
                                entryAllowed = 'Paso permitido'

                    # check black list
                    if name == 'Unknown' and bannedFaceEncondings:                                  # text equals to unknown bc that means there is not a result when the allowed list is checked
                        result = fr.compare_faces(bannedFaceEncondings, face_frame_encoding)
                        distances = fr.face_distance(bannedFaceEncondings, face_frame_encoding)
                        
                        if any(result):                      # check result in banned list
                            bestMatch = numpy.argmin(distances)
                            if result[bestMatch]:
                                name = f'{bannedNames[bestMatch]}'

                    # at this point, if its an allowed or banned person, it would have a name, so lets check if the name still being 'Unknown', that would say person is an strange
                    if name == "Unknown":
                        is_new_stranger = True

                        # check if its a new stranger or not
                        if strangersFaceEncodings:                      
                            result = fr.compare_faces(strangersFaceEncodings, face_frame_encoding)
                            if any(result):
                                is_new_stranger = False     # not new strange

                        if is_new_stranger:                 # new strange
                            strangersFaceEncodings.append(face_frame_encoding)
                            
                            uuid_gen = str(uuid.uuid4()).split('-')                     # split the code
                            randomSplit = random.randint(0, len(uuid_gen))-1            # create a rand number using the uuid len
                            filename = uuid_gen[randomSplit]                            # set the filename using the rad number

                            if face_locations:
                                # get the face coord
                                top, right, bottom, left = face_locations

                                # face cut
                                face_image = frame[top:bottom, left:right]

                                cv2.imwrite(f"{strangers_path}/{filename}.webp", face_image)          # save the face img

                    
                    # create the rectangle around the face
                    cv2.rectangle(frame,                                              # Select the image
                            (face_locations[3]-25, face_locations[0]-55),           # left,top coord
                            (face_locations[1]+25, face_locations[2]+25),           # right, bottom coord
                            color,                                            
                            2)                                                      # thickness

                    # create a rectagle with the name
                    cv2.rectangle(frame,                                            # Select the image
                            (face_locations[3]-25, face_locations[0]-85),         # left,top coord
                            (face_locations[1]+25, face_locations[0]-55),         # right, bottom coord
                            color,                                            
                            -1)                                                   # thickness (-1 to fill)
                    # calcs to center text
                    rect_top_left = (face_locations[3]-25, face_locations[0]-85)
                    rect_bottom_right = (face_locations[1]+25, face_locations[0]-55)
                    textCoords = get_centered_text_coordinates(rect_top_left, rect_bottom_right, name)

                    cv2.putText(frame, name, textCoords, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)


                    # create a rectagle to allow entrance or not
                    cv2.rectangle(frame,                                            # Select the image
                            (face_locations[3]-25, face_locations[2]+25),         # left,top coord
                            (face_locations[1]+25, face_locations[2]+55),         # right, bottom coord
                            color,                                            
                            -1)                                                   # thickness (-1 to fill)
                    rect_top_left = (face_locations[3]-25, face_locations[2]+25)
                    rect_bottom_right = (face_locations[1]+25, face_locations[2]+55)
                    textCoords = get_centered_text_coordinates(rect_top_left, rect_bottom_right, entryAllowed)

                    cv2.putText(frame, entryAllowed, textCoords, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)


                    # get the predominant emotion using fer
                    emotions = emotion_detector.detect_emotions(frame)
                    '''
                    detect_emotions(frame) take the frame as input, and returns a list with diferent emotions
                    [0] would process only the first face
                    ['emotions'] get the probability of every emotion detected
                    '''
                    
                    emotionText = 'emotionless, huhg?'

                    if emotions:   
                        pred_emotion = emotions[0]['emotions']                                         #check if exist any emotion
                        emotion = max(pred_emotion, key=pred_emotion.get)       # gets the emotion with the max probability
                        print(emotions)                                         # print all emotions
                        emotionText = emotion                                   # get the emotion
                    
                    # create a rectagle to show the emotion
                    cv2.rectangle(frame,                                             # Select the image
                            (face_locations[3]-25, face_locations[2]+55),          # left,top coord
                            (face_locations[1]+25, face_locations[2]+85),          # right, bottom coord
                            color,                                            
                            -1)                                                   # thickness (-1 to fill)
                    rect_top_left = (face_locations[3]-25, face_locations[2]+55)
                    rect_bottom_right = (face_locations[1]+25, face_locations[2]+85)
                    textCoords = get_centered_text_coordinates(rect_top_left, rect_bottom_right, emotionText)

                    cv2.putText(frame, emotionText, (face_locations[3]-15, face_locations[2]+80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                    # get how much faces are in front camera
                    hand_gesture = f'Posicion de la mano: {detect_hand_gesture(frame, hands, mp_hands, mp_drawing)}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.7
                    color = (255, 255, 255)  
                    thickness = 2
                    
                    # get the frame h and w
                    height, width = frame.shape[:2]

                    # show text
                    cv2.putText(frame, hand_gesture, (10, 60), font, font_scale, color, thickness)
                
            # show the frames
            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1)
            if k==27:
                break

    finally:
        video.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
