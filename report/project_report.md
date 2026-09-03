# PROJECT REPORT
## AI-Based Classroom Attendance from Face Recognition

### 1. Problem Statement
Manual classroom attendance consumes teaching time and can introduce errors. The proposed system automates attendance by detecting and recognizing registered student faces from a classroom photograph.

### 2. Objective
To build an AI-based classroom attendance system that detects and recognizes students, marks Present/Absent status, stores attendance records, and provides a teacher dashboard with CSV export.

### 3. Proposed System
The system has four major stages:
1. Student registration
2. Face detection
3. Face recognition
4. Attendance storage and reporting

### 4. System Architecture
Teacher → Flask Web Interface → OpenCV Face Detection → LBPH Recognition → SQLite Database → Teacher Dashboard → CSV Export.

### 5. Technologies
- Python
- Flask
- OpenCV
- LBPH Face Recognizer
- Haar Cascade face detector
- SQLite
- HTML/CSS
- CSV

### 6. Dataset Details
A registration-based dataset is used. Each student provides one clear front-facing image. The application detects the face and stores a cropped grayscale training sample associated with the student's internal label. For a formal accuracy study, collect multiple images per student under different lighting and poses and divide them into training and testing sets.

### 7. Methodology
**Registration:** Student details and face image are saved.  
**Detection:** Haar Cascade identifies face regions.  
**Recognition:** LBPH compares the detected face against registered samples.  
**Attendance:** Recognized labels are marked Present; other registered students are marked Absent.  
**Storage:** SQLite stores student and attendance records.  
**Dashboard:** The teacher can view, correct and export attendance.

### 8. Accuracy Evaluation
Accuracy should be calculated from a labeled test dataset:
Accuracy = Correct recognitions / Total test faces × 100.

The project intentionally does not insert a fabricated accuracy value. The final report should contain the measured result after testing with the collected dataset.

### 9. Advantages
- Reduces manual roll-call time
- Provides centralized attendance records
- Supports manual correction
- Allows CSV export
- Easy to demonstrate as a web application

### 10. Limitations
Recognition can be affected by lighting, camera quality, face angle, occlusion and limited training samples. LBPH is suitable for an academic prototype but is not the strongest choice for high-security production use.

### 11. Future Enhancements
- Live webcam attendance
- Multiple training images per student
- Deep-learning face embeddings
- Liveness/anti-spoofing
- Authentication for teachers
- Cloud database
- Monthly attendance analytics

### 12. Conclusion
The project demonstrates an end-to-end AI-assisted attendance workflow. Registered students can be recognized from a classroom image, attendance can be stored in SQLite, teachers can correct records, and reports can be exported as CSV.

### 13. Demo Video Plan (2–3 minutes)
**0:00–0:20** — Introduce the problem and project.  
**0:20–0:55** — Register two or more students.  
**0:55–1:35** — Upload a classroom image and run recognition.  
**1:35–2:15** — Show the dashboard and Present/Absent records.  
**2:15–2:35** — Correct one record manually.  
**2:35–2:55** — Export CSV and show the downloaded report.
