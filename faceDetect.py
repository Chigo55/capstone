import cv2
import mediapipe as mp

from collections import deque

# For webcam input:
def Detect(deque):
    try:
        mp_face_detection = mp.solutions.face_detection

        cap = cv2.VideoCapture(0)
        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.9) \
                as face_detection:

            print(f'detect start')
            while cap.isOpened():
                success, image = cap.read()

                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_detection.process(image)

                # Draw the face detection annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                h, w, _ = image.shape
                cv2.line(image, (int(w/2-100), 0), (int(w/2-100), int(h)), (0, 0, 255), 2)
                cv2.line(image, (int(w/2+100), 0), (int(w/2+100), int(h)), (0, 0, 255), 2)

                if results.detections:
                    bbox = results.detections[0].location_data.relative_bounding_box
                    

                    cv2.rectangle(image, (int(w * bbox.xmin), int(h * bbox.ymin)),
                                  (int(w * bbox.xmin) + int(w * bbox.width), int(h * bbox.ymin) + int(h * bbox.height)),
                                  (0, 0, 255), 2)

                    midpoint = (int((int(w * bbox.xmin) + int(w * bbox.xmin) + int(w * bbox.width))/2),
                                int((int(h * bbox.ymin) + int(h * bbox.ymin) + int(h * bbox.height))/2))

                    cv2.circle(image, midpoint, 2, (0, 0, 255), -1, cv2.LINE_AA)

                    deque.append([w, midpoint])
                
                else:
                    deque.append([w])

                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))

                if cv2.waitKey(1) == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break

    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        pass

if __name__ == '__main__':
    point = deque()
    Detect(point)
    print(point.popleft())
