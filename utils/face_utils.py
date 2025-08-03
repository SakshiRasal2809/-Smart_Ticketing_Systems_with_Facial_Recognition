import os
import cv2
import numpy as np

# Directory to store passenger face images
KNOWN_FACES_DIR = "known_faces"
FACE_SIZE = (100, 100)  # Cropped face size

# Create directory if it doesn't exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def capture_face(name):
    """
    Capture passenger's face from webcam, save it, and return image path.
    Press 's' to save the face, 'q' to quit without saving.
    """
    cap = cv2.VideoCapture(0)
    print("[INFO] Press 's' to save face, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF

        # Save face when 's' is pressed
        if key == ord('s') and len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, FACE_SIZE)
            path = os.path.join(KNOWN_FACES_DIR, f"{name}.png")
            cv2.imwrite(path, face_img)
            print(f"[INFO] Saved face for {name} at {path}")
            
            cap.release()
            cv2.destroyAllWindows()
            return path  # return path to store in DB

        # Quit without saving
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def recognize_face():
    """
    Recognize passenger from webcam by comparing with saved faces.
    Returns matched name or None.
    """
    # Load known faces
    known_faces = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            known_faces.append((img, os.path.splitext(filename)[0]))

    if not known_faces:
        print("[WARN] No registered faces found.")
        return None

    cap = cv2.VideoCapture(0)
    print("[INFO] Looking for face... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            detected_face = gray[y:y+h, x:x+w]
            detected_face = cv2.resize(detected_face, FACE_SIZE)

            # Compare with known faces
            for known_img, name in known_faces:
                diff = cv2.absdiff(known_img, detected_face)
                similarity = 1 - (np.sum(diff) / (255 * FACE_SIZE[0] * FACE_SIZE[1]))

                if similarity > 0.6:  # Match threshold
                    print(f"[INFO] Recognized: {name}")
                    cap.release()
                    cv2.destroyAllWindows()
                    return name

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
