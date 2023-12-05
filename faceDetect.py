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
            cv2.line(frame, (int(w/2-100), 0), (int(w/2-100), int(h)), (0, 0, 255), 2)
            cv2.line(frame, (int(w/2+100), 0), (int(w/2+100), int(h)), (0, 0, 255), 2)

            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                midpoint = (int((int(w * bbox.xmin) + int(w * bbox.xmin) + int(w * bbox.width))/2),
                                int((int(h * bbox.ymin) + int(h * bbox.ymin) + int(h * bbox.height))/2))
                cv2.rectangle(frame, (int(w * bbox.xmin), int(h * bbox.ymin)),
                                  (int(w * bbox.xmin) + int(w * bbox.width), int(h * bbox.ymin) + int(h * bbox.height)),
                                  (0, 0, 255), 2)
                cv2.circle(frame, midpoint, 2, (0, 0, 255), -1, cv2.LINE_AA)
                deque.append([w, midpoint])

            cv2.imshow('MediaPipe Face Detection', cv2.flip(frame, 1))

            if cv2.waitKey(1) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break