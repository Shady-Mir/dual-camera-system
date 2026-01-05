# dual-camera-system
Dual camera system on Raspberry Pi with a real-time graphical user interface (GUI), adjustable camera parameters, and synchronous image capture in TIFF format.
# Project Goals
- Development of a graphical user interface (GUI) that displays both camera streams simultaneously and in real time, side by side.
- Implementation of adjustable camera parameters for each camera:
- Exposure time
- Gain
- White balance
- Resolution
- Frame rate
- Storage location for captured images
- Implementation of a synchronous image capture mechanism where both cameras are triggered together and images are saved in TIFF format including timestamps.
# Implementation Overview
- The GUI is implemented using PyQt6.
- Dual camera control and configuration are implemented on Raspberry Pi.
- Camera parameters can be adjusted independently for each camera.
- The system supports real-time preview and synchronized image capture.
# Current Status and Next Steps
- Real-time dual camera streaming with adjustable parameters is implemented.
- Synchronous image capture in TIFF format is supported.
- Further evaluation and validation of camera synchronization accuracy is planned.
