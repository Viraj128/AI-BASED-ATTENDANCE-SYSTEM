#  AI-Based Smart Attendance System

##  Overview

This project is an **AI-powered attendance system** that automatically marks student attendance using **face recognition and liveness detection**.

Instead of traditional manual attendance, this system uses a webcam to:

* Detect faces
* Identify students
* Verify that the person is real (not photo/video)
* Mark attendance automatically

👉 The goal is to make attendance **secure, automated, and proxy-proof**.



##  Key Features

✅ Face Recognition-based Attendance
✅ Blink Detection (Liveness Check)
✅ Depth Detection (Anti-spoofing)
✅ Admin Panel (Manage users, subjects)
✅ Teacher Dashboard (Start live session)
✅ Manual Attendance Option
✅ Attendance Reports (Daily & Monthly)
✅ Student Enrollment with Images



##  How the System Works

### 🔹 Step 1: Enrollment

* Admin adds students
* Uploads multiple face images
* System stores images in `face_dataset/`
* AI converts images into **face encodings (numerical data)**

👉 These encodings are saved in:

```
encodings/encodings.pkl
```



### 🔹 Step 2: Start Live Session

* Teacher clicks **Start Session**
* Webcam starts automatically
* Live video feed is processed frame-by-frame

---

### 🔹 Step 3: Face Detection & Recognition

For every frame:

1. Face is detected
2. Face is converted into a **128-dimension encoding**
3. Compared with stored encodings

👉 If match found → student identified

---

### 🔹 Step 4: Liveness Detection (VERY IMPORTANT)

To prevent fake attendance:

#### 👁️ Blink Detection

* Detects eye movement using facial landmarks
* Ensures person is live

#### 🧍 Depth Detection

* Uses AI depth estimation
* Checks if face has 3D structure
* Rejects flat images/videos

---

### 🔹 Step 5: Attendance Marking

Attendance is marked ONLY if:

```
Face Matched ✅
+ Blink Detected ✅
+ Depth Verified ✅
```

👉 Then:

* Attendance stored in database
* Timestamp + Date saved

---

##  How AI is Used in This System

This system uses **Artificial Intelligence (AI)** in multiple stages:

---

### 🔹 1. Face Recognition

* Converts face into numerical features
* Compares with stored data
* Identifies the person

👉 Uses:

* Machine Learning
* Computer Vision

---

### 🔹 2. Facial Landmark Detection

* Detects eyes, nose, face structure
* Used for blink detection

---

### 🔹 3. Liveness Detection

#### ✔ Blink Detection

* Detects real eye movement

#### ✔ Depth Estimation (MiDaS Model)

* Predicts 3D depth from 2D image
* Differentiates real face vs screen

---

### 🔹 4. Decision Logic

System intelligently decides:

```
IF (Face Match AND Real Person)
→ Mark Attendance
ELSE
→ Ignore
```

👉 This is AI-based decision making.

---

##  Technologies Used

###  Backend

* Python
* Flask

###  AI & Computer Vision

* OpenCV
* dlib
* face_recognition
* PyTorch
* MiDaS (Depth Estimation)

###  Database

* SQLite3

###  Frontend

* HTML
* CSS (Bootstrap)

---

## 📂 Project Structure

```
attendance_system/
│
├── app.py
├── database_manager.py
├── attendance.db
│
├── ai_modules/
│   ├── face_recognition.py
│   ├── liveness_detection.py
│
├── face_dataset/
├── encodings/
├── models/
│
├── templates/
├── static/
```

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```
pip install flask opencv-python face-recognition dlib torch torchvision timm
```

---

### 2️⃣ Initialize Database

```
python init_db.py
```

---

### 3️⃣ Run the Application

```
python app.py
```

---

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---



##  Limitations

* Requires good lighting
* Depth detection needs extra dependencies
* Slight delay due to heavy AI models

---

##  Future Improvements

* Mobile app integration
* Cloud database (Firebase / MongoDB)
* Faster AI models
* Multi-camera support
* Face mask detection
* Prevents proxy attendance
* Detects fake images/videos
* Requires real human interaction
* Multi-layer verification
 
 


##  Conclusion

This system demonstrates how **Artificial Intelligence can automate real-world tasks** like attendance while ensuring security.

👉 It is not just face detection, but a **complete intelligent system** that:

* Identifies users
* Verifies authenticity
* Prevents fraud
* Automates records

---


