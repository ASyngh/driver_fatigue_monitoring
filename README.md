# 🚗 Driver Fatigue Monitoring System

A real-time driver drowsiness detection system built using OpenCV and MediaPipe.

## 🔍 Overview

This system monitors a driver using a webcam and detects fatigue based on:

- Eye closure (EAR - Eye Aspect Ratio)
- Yawning (MAR - Mouth Aspect Ratio)
- Forward head droop (Geometric head-drop detection)

It uses adaptive auto-calibration to personalize detection thresholds for each user.

---

## 🧠 Features

- Real-time face landmark tracking (MediaPipe FaceMesh)
- Adaptive 5-second user calibration
- Multi-signal fatigue fusion logic
- NORMAL / WARNING / CRITICAL state classification
- Audio alert system
- Session logging (CSV export)
- Modular clean architecture

---

## ⚙️ Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- playsound
- Git

---


---

## 🚀 How It Works

1. The system performs a 5-second calibration.
2. It dynamically computes personalized thresholds.
3. Real-time monitoring begins.
4. Fatigue signals are fused into a severity score.
5. Alerts trigger on WARNING / CRITICAL states.
6. Session summary is logged to CSV.

---

## 📊 Output

At the end of each session:

- Duration
- Eye closure events
- Yawn events
- Head droop events
- Critical fatigue events

are saved in `logs/session_logs.csv`.

---

## 🔔 Alert System

- WARNING → soft audio alert
- CRITICAL → stronger alert
- No alert spamming (state transition-based)

---

## 📌 Future Improvements

- Fatigue score visualization bar
- Session analytics dashboard
- Automatic driver profile storage
- Deployment-ready UI

---

## 👨‍💻 Author

Aditya Singh
