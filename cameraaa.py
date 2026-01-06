# cameraaa.py
import cv2
from picamera2 import Picamera2
import threading

_cam0: Picamera2 | None = None
_cam1: Picamera2 | None = None

_lock = threading.Lock() 


_state = {
    0: {"size": (640, 480), "fps": 30, "awb": "Auto", "exposure_us": 10000, "gain": 1.0},
    1: {"size": (640, 480), "fps": 30, "awb": "Auto", "exposure_us": 10000, "gain": 1.0},
}

_AWB_MAP = {
    "Auto": 0,
    "Daylight": 1,
    "Cloudy": 2,
    "Tungsten": 3,
    "Fluorescent": 4,
}

def _get_cam(idx: int) -> Picamera2:
    global _cam0, _cam1
    if idx == 0:
        if _cam0 is None:
            raise RuntimeError("Cam0 not initialized")
        return _cam0
    if idx == 1:
        if _cam1 is None:
            raise RuntimeError("Cam1 not initialized")
        return _cam1
    raise ValueError("Camera index must be 0 or 1")

def _apply_controls(idx: int):
    """Apply controls safely. Must be called inside lock by caller or we lock here."""
    cam = _get_cam(idx)
    st = _state[idx]

    fps = int(st["fps"])
    frame_us = int(1_000_000 / max(1, fps)) 

    exp = max(500, int(st["exposure_us"]))      
    gain = max(1.0, float(st["gain"]))       

    controls = {
        "ExposureTime": exp,                        
        "AnalogueGain": gain,
        "AwbMode": int(_AWB_MAP.get(st["awb"], 0)),
        "FrameDurationLimits": (frame_us, frame_us) 
    }
    cam.set_controls(controls)

def _reconfigure(idx: int):
    cam = _get_cam(idx)
    st = _state[idx]
    size = st["size"]

    cam.stop()
    cfg = cam.create_video_configuration(
        main={"size": size, "format": "BGR888"}   
    )
    cam.configure(cfg)
    cam.start()
    _apply_controls(idx)


def init_cameras(size=(640, 480), fps=30):       #GUIIIIII
    global _cam0, _cam1
    _state[0]["size"] = tuple(size)
    _state[1]["size"] = tuple(size)
    _state[0]["fps"] = int(fps)
    _state[1]["fps"] = int(fps)

    _cam0 = Picamera2(0)
    _cam1 = Picamera2(1)

    cfg0 = _cam0.create_video_configuration(main={"size": size, "format": "BGR888"})  # ✅
    cfg1 = _cam1.create_video_configuration(main={"size": size, "format": "BGR888"})  # ✅
    _cam0.configure(cfg0)
    _cam1.configure(cfg1)

    _cam0.start()
    _cam1.start()

    _apply_controls(0)
    _apply_controls(1)
    return True

def set_exposure(idx: int, exposure_us: int):
    with _lock:
        _state[idx]["exposure_us"] = int(exposure_us)
        _apply_controls(idx)

def set_gain(idx: int, gain: float):
    with _lock:
        _state[idx]["gain"] = float(gain)
        _apply_controls(idx)

def set_awb(idx: int, awb_name: str):
    with _lock:
        _state[idx]["awb"] = str(awb_name)
        _apply_controls(idx)

def set_fps(idx: int, fps: int):
   
    with _lock:         
        _state[idx]["fps"] = int(fps)
        _apply_controls(idx)

def set_resolution(idx: int, size: tuple[int, int]):
    with _lock:
        _state[idx]["size"] = (int(size[0]), int(size[1]))
        _reconfigure(idx)

def get_frame(idx: int):
    with _lock:
        cam = _get_cam(idx)
        bgr = cam.capture_array()
    return bgr

def capture_tiff_pair(path0: str, path1: str):    #TIFFFFFFFFF
    with _lock:
        img0 = cv2.cvtColor(_get_cam(0).capture_array(), cv2.COLOR_RGB2BGR)
        img1 = cv2.cvtColor(_get_cam(1).capture_array(), cv2.COLOR_RGB2BGR)

    cv2.imwrite(path0, img0)
    cv2.imwrite(path1, img1)
