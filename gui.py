from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QSlider, QComboBox, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
import cv2
import os
from datetime import datetime

from cameraaa import init_cameras, get_frame 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
   
        init_cameras()
        self.setWindowTitle("Dual Camera System – Simulation")

        
        self.cam1_label = QLabel("Camera 0")
        self.cam1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam1_label.setStyleSheet("border: 2px solid black;")
        self.cam1_label.setFixedSize(400, 300)

        self.cam1_exp_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam1_exp_slider.setRange(0, 100)
        self.cam1_exp_slider.setValue(50)

        self.cam1_gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam1_gain_slider.setRange(0, 100)
        self.cam1_gain_slider.setValue(50)

        self.cam1_res_box = QComboBox()
        self.cam1_res_box.addItems(["640x480", "800x600", "1280x720"])
        
        self.cam1_wb_box = QComboBox()
        self.cam1_wb_box.addItems(["Auto", "Daylight", "Cloudy", "Fluorescent", "Tungsten"])

        self.cam1_fps_box = QComboBox()
        self.cam1_fps_box.addItems(["15", "30", "60"])

        cam1_layout = QVBoxLayout()
        cam1_layout.addWidget(self.cam1_label)
        cam1_layout.addWidget(QLabel("Exposure"))
        cam1_layout.addWidget(self.cam1_exp_slider)
        cam1_layout.addWidget(QLabel("Gain"))
        cam1_layout.addWidget(self.cam1_gain_slider)
        cam1_layout.addWidget(QLabel("White balance"))
        cam1_layout.addWidget(self.cam1_wb_box)
        cam1_layout.addWidget(QLabel("Resolution"))
        cam1_layout.addWidget(self.cam1_res_box)
        cam1_layout.addWidget(QLabel("FPS"))
        cam1_layout.addWidget(self.cam1_fps_box)

        cam1_widget = QWidget()
        cam1_widget.setLayout(cam1_layout)

      
        self.cam2_label = QLabel("Camera 1")
        self.cam2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam2_label.setStyleSheet("border: 2px solid black;")
        self.cam2_label.setFixedSize(400, 300)

        self.cam2_exp_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam2_exp_slider.setRange(0, 100)
        self.cam2_exp_slider.setValue(50)

        self.cam2_gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam2_gain_slider.setRange(0, 100)
        self.cam2_gain_slider.setValue(50)

        self.cam2_res_box = QComboBox()
        self.cam2_res_box.addItems(["640x480", "800x600", "1280x720"])
        
        self.cam2_wb_box = QComboBox()
        self.cam2_wb_box.addItems(["Auto", "Daylight", "Cloudy", "Fluorescent", "Tungsten"])

        self.cam2_fps_box = QComboBox()
        self.cam2_fps_box.addItems(["15", "30", "60"])

        cam2_layout = QVBoxLayout()
        cam2_layout.addWidget(self.cam2_label)
        cam2_layout.addWidget(QLabel("Exposure"))
        cam2_layout.addWidget(self.cam2_exp_slider)
        cam2_layout.addWidget(QLabel("Gain"))
        cam2_layout.addWidget(self.cam2_gain_slider)
        cam2_layout.addWidget(QLabel("White balance"))
        cam2_layout.addWidget(self.cam2_wb_box)
        cam2_layout.addWidget(QLabel("Resolution"))
        cam2_layout.addWidget(self.cam2_res_box)
        cam2_layout.addWidget(QLabel("FPS"))
        cam2_layout.addWidget(self.cam2_fps_box)

        cam2_widget = QWidget()
        cam2_widget.setLayout(cam2_layout)

      
        self.capture_btn = QPushButton("Capture synchronously")

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Storage folder (default: current folder)")
        self.browse_btn = QPushButton("Browse...")

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Storage path:"))
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_btn)

       
        h = QHBoxLayout()
        h.addWidget(cam1_widget)
        h.addWidget(cam2_widget)

        v = QVBoxLayout()
        v.addLayout(h)
        v.addLayout(path_layout)
        v.addWidget(self.capture_btn)

        self.setLayout(v)

       
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_images)
        self.timer.start(50)  

        self.capture_btn.clicked.connect(self.capture_images)
        self.browse_btn.clicked.connect(self.choose_folder)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select storage folder")
        if folder:
            self.path_edit.setText(folder)


    def update_images(self):
        img1 = get_frame(0)  
        img2 = get_frame(1)  

        self.cam1_label.setPixmap(self.to_pixmap(img1))
        self.cam2_label.setPixmap(self.to_pixmap(img2))

    def to_pixmap(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(img)

  
    def capture_images(self):
     
        settings_cam0 = {
            "exposure": self.cam1_exp_slider.value(),
            "gain": self.cam1_gain_slider.value(),
            "white_balance": self.cam1_wb_box.currentText(),
            "resolution": self.cam1_res_box.currentText(),
            "fps": self.cam1_fps_box.currentText(),
        }
        settings_cam1 = {
            "exposure": self.cam2_exp_slider.value(),
            "gain": self.cam2_gain_slider.value(),
            "white_balance": self.cam2_wb_box.currentText(),
            "resolution": self.cam2_res_box.currentText(),
            "fps": self.cam2_fps_box.currentText(),
        }
        print("Cam0 settings:", settings_cam0)
        print("Cam1 settings:", settings_cam1)

      
        img1 = get_frame(0)
        img2 = get_frame(1)
        
      
        folder = self.path_edit.text().strip() or "."
        os.makedirs(folder, exist_ok=True)

       
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        file0 = os.path.join(folder, f"cam0_{ts}.tiff")
        file1 = os.path.join(folder, f"cam1_{ts}.tiff")

        cv2.imwrite(file0, img1)
        cv2.imwrite(file1, img2)

        print("Saved:", file0)
        print("Saved:", file1)
