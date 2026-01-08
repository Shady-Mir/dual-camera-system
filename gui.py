from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QSlider, QComboBox, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
import cv2
import os
from datetime import datetime

from cameraaa import (
    init_cameras, get_frame,
    set_exposure, set_gain, set_awb, set_resolution, set_fps,
    capture_tiff_pair
)

def parse_res(text: str):
    w, h = text.lower().split("x")
    return int(w), int(h)


class MainWindow(QWidget) :
    def __init__(self):
        super().__init__()

        init_cameras(size=(640, 480), fps=30)   #default cam setttt
        self.setWindowTitle("Dual Camera System")

        # CAMMMMMMMMM 0 
        self.cam1_label = QLabel("Camera 0")
        self.cam1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cam1_label.setStyleSheet("border: 2px solid black;")
        self.cam1_label.setFixedSize(400, 300)

        self.cam1_exp_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam1_exp_slider.setRange(100, 30000)     
        self.cam1_exp_slider.setValue(10000)

        self.cam1_gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam1_gain_slider.setRange(10, 160)      
        self.cam1_gain_slider.setValue(10)  

        self.cam1_wb_box = QComboBox()
        self.cam1_wb_box.addItems(["Auto", "Daylight", "Cloudy", "Fluorescent", "Tungsten"])

        self.cam1_res_box = QComboBox()
        self.cam1_res_box.addItems(["640x480", "800x600", "1280x720"])

        self.cam1_fps_box = QComboBox()
        self.cam1_fps_box.addItems(["15", "30", "60"])
        self.cam1_fps_box.setCurrentText("30")
        self.cam1_exp_label = QLabel(f"Exposure (us): {self.cam1_exp_slider.value()} µs")
        self.cam1_gain_label = QLabel(f"Gain: {self.cam1_gain_slider.value()/10:.1f}×"
        
)

        cam1_layout = QVBoxLayout()
        cam1_layout.addWidget(self.cam1_label)
        cam1_layout.addWidget(self.cam1_exp_label)
        cam1_layout.addWidget(self.cam1_exp_slider)
        cam1_gain_layout = QHBoxLayout()
        cam1_gain_layout.addWidget(self.cam1_gain_label)
        cam1_gain_layout.addWidget(self.cam1_gain_slider)
        cam1_layout.addLayout(cam1_gain_layout)
        cam1_layout.addWidget(QLabel("White balance"))
        cam1_layout.addWidget(self.cam1_wb_box)
        cam1_layout.addWidget(QLabel("Resolution"))
        cam1_layout.addWidget(self.cam1_res_box)
        cam1_layout.addWidget(QLabel("FPS"))
        cam1_layout.addWidget(self.cam1_fps_box)
        cam1_widget = QWidget()
        cam1_widget.setLayout(cam1_layout)
        self.cam1_gain_slider.valueChanged.connect(
            lambda v: (
                self.cam1_gain_label.setText(f"Gain: {v/10:.1f}×"),
                set_gain(1, v/10.0)
            )
        )      

        # CAMMMMMMMMM 1 
        self.cam2_label = QLabel("Camera 1")
        self.cam2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.cam2_label.setStyleSheet("border: 2px solid black;")
        self.cam2_label.setFixedSize(400, 300)

        self.cam2_exp_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam2_exp_slider.setRange(100, 30000)
        self.cam2_exp_slider.setValue(10000)

        self.cam2_gain_slider = QSlider(Qt.Orientation.Horizontal)
        self.cam2_gain_slider.setRange(10, 160)
        self.cam2_gain_slider.setValue(10)

        self.cam2_wb_box = QComboBox()
        self.cam2_wb_box.addItems(["Auto", "Daylight", "Cloudy", "Fluorescent", "Tungsten"])

        self.cam2_res_box = QComboBox()
        self.cam2_res_box.addItems(["640x480", "800x600", "1280x720"])

        self.cam2_fps_box = QComboBox()
        self.cam2_fps_box.addItems(["15", "30", "60"])
        self.cam2_fps_box.setCurrentText("30")
        self.cam2_exp_label = QLabel(f"Exposure (us): {self.cam2_exp_slider.value()} µs")
        self.cam2_gain_label = QLabel(f"Gain: {self.cam2_gain_slider.value()/10:.1f}×"
)

        cam2_layout = QVBoxLayout()
        cam2_layout.addWidget(self.cam2_label)
        cam2_layout.addWidget(self.cam2_exp_label)
        cam2_layout.addWidget(self.cam2_exp_slider)
        cam2_gain_layout = QHBoxLayout()
        cam2_gain_layout.addWidget(self.cam2_gain_label)
        cam2_layout.addLayout(cam2_gain_layout)
        self.cam2_gain_slider.valueChanged.connect(
            lambda v: (
                self.cam2_gain_label.setText(f"Gain: {v/10:.1f}×"),
                set_gain(1, v/10.0)
            )
        )      
        cam2_layout.addWidget(self.cam2_gain_slider)
        cam2_layout.addWidget(QLabel("White balance"))
        cam2_layout.addWidget(self.cam2_wb_box)
        cam2_layout.addWidget(QLabel("Resolution"))
        cam2_layout.addWidget(self.cam2_res_box)
        cam2_layout.addWidget(QLabel("FPS"))
        cam2_layout.addWidget(self.cam2_fps_box)
        cam2_widget = QWidget()
        cam2_widget.setLayout(cam2_layout)

        # CAPTUREEEEEEEEE
        self.capture_btn = QPushButton("Capture synchronously (TIFF)")

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

        # PIC UPDATEEEEEE
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_images)
        self.timer.start(50)

        self.cam1_exp_slider.valueChanged.connect(
            lambda val: (
                self.cam1_exp_label.setText(f"Exposure (us): {val} µs"),
                set_exposure(0, val)
            )
        )
        self.cam2_exp_slider.valueChanged.connect(
            lambda val: (
                self.cam2_exp_label.setText(f"Exposure (us): {val} µs"),
                set_exposure(1, val)
            )
        )


        self.cam1_wb_box.currentTextChanged.connect(lambda t: set_awb(0, t))
        self.cam2_wb_box.currentTextChanged.connect(lambda t: set_awb(1, t))

        self.cam1_fps_box.currentTextChanged.connect(lambda t: set_fps(0, int(t)))
        self.cam2_fps_box.currentTextChanged.connect(lambda t: set_fps(1, int(t)))

        self.cam1_res_box.currentTextChanged.connect(lambda t: set_resolution(0, parse_res(t)))
        self.cam2_res_box.currentTextChanged.connect(lambda t: set_resolution(1, parse_res(t)))

        # BUTTONSSSSSSSSSSS
        self.capture_btn.clicked.connect(self.capture_images)
        self.browse_btn.clicked.connect(self.choose_folder)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select storage folder")
        if folder:
            self.path_edit.setText(folder)

    def update_images(self): #STREAMMMMMM
        try:
            img1 = get_frame(0)
            self.cam1_label.setPixmap(self.to_pixmap(img1))
        except Exception as e:
            self.cam1_label.setText(f"Cam0 NOT connected\n{e}")

        
        try:
            img2 = get_frame(1)
            self.cam2_label.setPixmap(self.to_pixmap(img2))
        except Exception as e:
            self.cam2_label.setText(f"Cam1 NOT connected\n{e}")

    def to_pixmap(self, frame):
        if not frame.flags["C_CONTIGUOUS"]:   #IN ORDERRRRRR
            frame = frame.copy()

        h, w, ch = frame.shape

        bytes_per_line = ch * w   

        qimg = QImage(
            frame.data,
            w,
            h,
            bytes_per_line,
            QImage.Format.Format_BGR888
        ).copy()   #SAFE 

        return QPixmap.fromImage(qimg).scaled(
            self.cam1_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )


    def capture_images(self):
        folder = self.path_edit.text().strip() or "."
        os.makedirs(folder, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file0 = os.path.join(folder, f"cam0_{ts}.tiff")
        file1 = os.path.join(folder, f"cam1_{ts}.tiff")

        capture_tiff_pair(file0, file1)
        print("Saved:", file0)
        print("Saved:", file1)
