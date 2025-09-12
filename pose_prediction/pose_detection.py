import cv2
import numpy as np
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

source = "../videos/1.mp4"

cap = cv2.VideoCapture(source)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'MP4V') # Or 'XVID', 'MJPG', etc.
out = cv2.VideoWriter('../output/output_video.mp4', fourcc, fps, (width, height))

with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())
            
            cv2.imshow("Pose Detection", image)
            out.write(image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        else:
            break

cap.release()
out.release()
cv2.destroyAllWindows()
