import face_recognition
import os
import pickle

path = "dataset/"
known_encodings = []
known_names = []

# Loop through all student folders
for student in os.listdir(path):
    student_path = os.path.join(path, student)
    if not os.path.isdir(student_path):
        continue

    # Loop through all images of each student
    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)
        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(student)

# Save encodings
data = {"encodings": known_encodings, "names": known_names}
with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("✅ Training complete! Encodings saved to encodings.pkl")
