# AI-Based Classroom Attendance from Face Recognition

## Student
**Name:** HEMALATHA.A  
**Register No:** 212224240056

## Objective
To build a system that automatically marks classroom attendance using AI-based face recognition, reducing manual roll-call time and improving accuracy.

## Features
- Student registration with face image
- Classroom photo upload
- Face detection using OpenCV Haar Cascade
- Face recognition using LBPH
- Automatic Present/Absent marking
- SQLite attendance database
- Teacher dashboard
- Manual attendance correction
- CSV export

## Architecture
```text
Teacher
   |
   v
Flask Web Dashboard
   |
   +--> Student Registration --> Face Detection --> LBPH Model
   |
   +--> Classroom Image --> Face Detection --> Face Recognition
   |                                      |
   |                                      v
   |                               Present/Absent
   |
   +--> Dashboard --> SQLite Database --> CSV Export
```

## Dataset
This project uses a small registration-based dataset. The teacher registers each student using a clear face photograph. The registered images are used to train the LBPH recognizer. No external personal dataset is required.

For a real deployment, obtain consent and follow institutional privacy/data-retention rules.

## Installation
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
5. Install packages:
   `pip install -r requirements.txt`
6. Run:
   `python app.py`
7. Open the local Flask address shown in the terminal.

## Usage
1. Open **Register** and add each student with a clear front-facing photo.
2. Open **Mark Attendance** and upload a classroom photo.
3. The system detects faces and compares them with registered face samples.
4. The dashboard shows Present/Absent status.
5. A teacher can manually correct a record.
6. Click **Export CSV** to download the attendance report.

## Accuracy
For an academic demonstration, evaluate the model with a separate test set of labeled classroom/student images. Report:
- Recognition accuracy = correctly recognized faces / total test faces × 100
- False acceptance rate
- False rejection rate

Do not claim a measured accuracy unless it has been experimentally evaluated on your dataset.

## Limitations
- LBPH performance can decrease with poor lighting, pose changes, occlusion, or low-resolution images.
- This demo uses one registered photo per student.
- Real-time camera support can be added using OpenCV VideoCapture.
- Production systems should use stronger face-recognition models, liveness detection, access control, encryption, and appropriate consent/privacy practices.

## Project Deliverables
- Source code
- Sample SQLite database
- Registration-based dataset structure
- Web dashboard
- CSV export
- Project report
