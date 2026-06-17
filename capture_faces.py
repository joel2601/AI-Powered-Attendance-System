# capture_faces.py
# Kubuntu-friendly face capture script

import os
import cv2
import time

# Force Qt to use X11 backend on Kubuntu
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")

path = "dataset/"

# Get student name
name = input("Enter student name: ").strip()

if not name:
    print("Name cannot be empty. Exiting.")
    exit(1)

# Create folder for student
os.makedirs(os.path.join(path, name), exist_ok=True)

# Open webcam
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("❌ Could not open camera.")
    exit(1)

count = 0

print("\nPress 'c' to capture an image")
print("Press 'q' to quit\n")

# Test GUI
use_gui = True

try:
    ret, frame = cam.read()

    if not ret:
        raise RuntimeError("Camera read failed.")

    cv2.imshow("Test Window", frame)
    cv2.waitKey(100)
    cv2.destroyWindow("Test Window")

except Exception as e:
    print("⚠️ GUI not available:", e)
    use_gui = False

# Manual capture mode
if use_gui:
    try:
        while True:
            ret, frame = cam.read()

            if not ret:
                print("❌ Camera read failed.")
                break

            cv2.imshow("Capturing Faces", frame)

            key = cv2.waitKey(20) & 0xFF

            # Exit if window closed
            if cv2.getWindowProperty(
                "Capturing Faces",
                cv2.WND_PROP_VISIBLE
            ) < 1:
                print("Window closed.")
                break

            if key == ord('c'):
                img_name = os.path.join(
                    path,
                    name,
                    f"{count}.jpg"
                )

                cv2.imwrite(img_name, frame)

                print(f"✅ Captured: {img_name}")

                count += 1

            elif key == ord('q'):
                print("👋 Quitting...")
                break

    except Exception as e:
        print("⚠️ Error during capture:", e)

    finally:
        cam.release()
        cv2.destroyAllWindows()

# Automatic fallback mode
if count == 0:
    print("\nNo manual captures detected.")
    print("Starting automatic capture of 10 images...\n")

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("❌ Could not open camera.")
        exit(1)

    for i in range(10):
        ret, frame = cam.read()

        if not ret:
            print("❌ Camera read failed.")
            break

        img_name = os.path.join(
            path,
            name,
            f"auto_{i}.jpg"
        )

        cv2.imwrite(img_name, frame)

        print(f"📸 Saved: {img_name}")

        time.sleep(0.7)

    cam.release()

    print("\n✅ Automatic capture completed.")

else:
    print(
        f"\n✅ Captured {count} images for {name}\n"
        f"Saved in: {os.path.join(path, name)}"
    )