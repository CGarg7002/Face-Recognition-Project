# 🧑‍💻✅ Attendance via Face Recognition System
A fully deployable desktop application which I initially built for my university. The application can help schools, workplaces, prisons to manage attendance of entities.

![Status](https://img.shields.io/badge/Status-Complete-green)
![Python](https://img.shields.io/badge/language-Python-blue)

## ⚙️🛠️ Features & Working
![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog11.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog11.png)
- **Add & Remove**: Functionality to add and remove an entity from the database.

![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog13.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog13.png)
- **Current Status**: This Feature allows you to see all the actions the application is performing under the hood, like in the above images it showed that a face has been recognized and whether that face is registered in the database or not.

![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog14.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog14.png)
- **Camera footage**: This shows what the camera is capturing with the names of the detected and registered face and "Unknown" for the faces that are not recognized.<br>

**NOTE**: The camera feed will not show up until a face is shown to the camera. This has been implemened to keep it resource efficient.

![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog10.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog10.png)
- **Preview**: This feature allows you to see the Preview of the attendance without downloading it.

![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog15.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog15.png)
- **Download**: This feature allows you to Download/Export the Attendance to a configurable Excel file to the directory you want.

![\CGarg7002\Attendance_via_Face_Recognition_System\screenshots\face_recog16.png](https://raw.githubusercontent.com/GargEngineers7002/Attendance_via_Face_Recognition_System/40f71cade13c8138307dab5a79f46c5731d38dab/screenshots/face_recog16.png)
- **Storage**: The application data is stored in the following directories on your device:
    - **Windows**:``` C:\Users\10\AppData\Local\Attendance System\Attendance System ```
    - **Linux**:``` ~/Library/Application Support/Attendance System/Attendance System ```
    - **Mac**:``` ~/.local/share/Attendance System/Attendance System ```

## 🛠️🚀 Building & Usage
- Clone the repository.
- 

## 📁 Project Files

```
ATTENDANCE_VIA_FACE_RECOGNITION_SYSTEM/
├── screenshots/
│   ├── face_recog10.png
│   ├── face_recog11.png
│   ├── face_recog12.png
│   ├── face_recog13.png
│   ├── face_recog14.png
│   ├── face_recog15.png
│   └── face_recog16.png
│
├── src/
│   ├── attendance.py
│   ├── data_dirs_manager.py
│   ├── main.py
│   └── recognitions.py
│
├── .gitignore
├── environment.yml
├── LICENSE
└── README.md
```

---

⭐ **Star this project if you found it helpful!**