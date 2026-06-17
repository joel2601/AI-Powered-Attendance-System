# Face Recognition Attendance System

A Python-based attendance system that uses face recognition to automatically identify students and record attendance.

## Features

- Capture student face images
- Train face recognition model
- Real-time face detection and recognition
- Automatic attendance marking
- Attendance export to CSV

## Project Structure

```
project/
│
├── dataset/
│   ├── Joel/
│   ├── Navaneeth/
│
├── capture_faces.py
├── train_model.py
├── attendance_system.py
├── encodings.pkl
├── attendance.csv
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd project

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

### Step 1: Capture Faces

```bash
python capture_faces.py
```

### Step 2: Train Model

```bash
python train_model.py
```

### Step 3: Run Attendance System

```bash
python attendance_system.py
```

### Output

Attendance is stored in:

```text
attendance.csv
```

## Technologies Used

- Python
- OpenCV
- face_recognition
- NumPy
- Pandas