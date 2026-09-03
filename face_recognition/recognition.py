import cv2
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
MODEL = BASE / "face_model.yml"
DATASET = BASE / "dataset" / "students"

def model_available():
    return hasattr(cv2, "face") and hasattr(cv2.face, "LBPHFaceRecognizer_create")

def detect_faces(gray):
    cascade = cv2.CascadeClassifier(CASCADE)
    return cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80,80))

def register_face(image_path, label):
    if not model_available():
        raise RuntimeError("Install opencv-contrib-python (not opencv-python).")
    img = cv2.imread(image_path)
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    if len(faces) == 0:
        return False
    x,y,w,h = max(faces, key=lambda r:r[2]*r[3])
    crop = gray[y:y+h, x:x+w]
    cv2.imwrite(str(DATASET / f"_label_{label}.jpg"), crop)
    train_model()
    return True

def train_model():
    if not model_available():
        raise RuntimeError("Install opencv-contrib-python.")
    faces, labels = [], []
    for p in DATASET.glob("_label_*.jpg"):
        label = int(p.stem.split("_")[-1])
        img = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            faces.append(img)
            labels.append(label)
    if faces:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(labels))
        recognizer.write(str(MODEL))

def recognize_faces(image_path, threshold=75):
    if not model_available():
        raise RuntimeError("Install opencv-contrib-python.")
    if not MODEL.exists():
        return set()
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the image.")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL))
    labels = set()
    for (x,y,w,h) in detect_faces(gray):
        label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        if confidence <= threshold:
            labels.add(int(label))
    return labels
