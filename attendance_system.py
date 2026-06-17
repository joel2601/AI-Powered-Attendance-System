import face_recognition
import cv2
import numpy as np
import pickle
import pandas as pd
from datetime import datetime

# Load trained encodings
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)

cam = cv2.VideoCapture(0)

attendance = []

print("Press 'q' to quit")

while True:
    ret, frame = cam.read()

    if not ret:
        break

    # Resize frame for faster and often more stable recognition
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(
        rgb_small,
        face_locations
    )

    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        name = "Unknown"

        face_distances = face_recognition.face_distance(
            data["encodings"],
            face_encoding
        )

        if len(face_distances) > 0:

            best_match_index = np.argmin(face_distances)
            best_distance = face_distances[best_match_index]

            # Lower threshold = fewer wrong matches
            if best_distance < 0.45:
                name = data["names"][best_match_index]

                if name not in [x["Name"] for x in attendance]:
                    now = datetime.now()

                    attendance.append({
                        "Name": name,
                        "Time": now.strftime("%H:%M:%S"),
                        "Date": now.strftime("%Y-%m-%d")
                    })

                    print(
                        f"Attendance marked for "
                        f"{name} "
                        f"(distance={best_distance:.3f})"
                    )

        top, right, bottom, left = face_location

        # Scale back to original frame size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

df = pd.DataFrame(attendance)
df.to_csv("attendance.csv", index=False)

print("Attendance saved to attendance.csv")