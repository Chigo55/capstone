import mediapipe as mp
import cv2

# face detect 함수
def faceDetect(deque):
    mp_face_detection = mp.solutions.face_detection

    with mp_face_detection.FaceDetection(model_selection=1,  min_detection_confidence=0.9) as face_detection:
        cap = cv2.VideoCapture(0)

        print(f'Detect Start')
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Ignoring empty camera frame.")
                continue

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            h, w, _ = frame.shape

            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                midpoint = (int((int(w * bbox.xmin) + int(w * bbox.xmin) + int(w * bbox.width))/2),
                                int((int(h * bbox.ymin) + int(h * bbox.ymin) + int(h * bbox.height))/2))
                deque.append([w, midpoint])
            
            else:
                deque.append([w])