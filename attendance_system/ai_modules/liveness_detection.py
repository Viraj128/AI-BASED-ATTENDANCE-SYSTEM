# attendance_system/ai_modules/liveness_detection.py
import cv2
import numpy as np
import dlib
from scipy.spatial import distance as dist

# You need shape_predictor_68_face_landmarks.dat -> download manually and place path here
SHAPE_PREDICTOR_PATH = "c:/Users/viraj/Downloads/attendance_system/attendance_system/models/shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = None
try:
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
except Exception as e:
    print("dlib predictor not found; liveness blink detection won't work until you download the model:", e)

# Eye aspect ratio helper
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    eps = 1e-6
    return (A + B) / (2.0 * (C + eps))

# Indexes for 68-landmark model
LEFT_EYE_IDX = list(range(36, 42))
RIGHT_EYE_IDX = list(range(42, 48))

# Simple blink detector: count frames with EAR < threshold
EAR_THRESHOLD = 0.22
CONSEC_FRAMES = 2

class BlinkDetector:
    def __init__(self):
        self.counter = 0
        self.blinks = 0

    def process(self, gray_frame, rect):
        """
        rect: dlib rectangle or (top,right,bottom,left)
        returns True if blink detected recently (i.e., we saw a blink)
        """
        if predictor is None:
            return False
        if isinstance(rect, tuple):
            top, right, bottom, left = rect
            rect_dlib = dlib.rectangle(left, top, right, bottom)
        else:
            rect_dlib = rect

        shape = predictor(gray_frame, rect_dlib)
        coords = []
        for i in range(0,68):
            coords.append((shape.part(i).x, shape.part(i).y))
        leftEye = [coords[i] for i in LEFT_EYE_IDX]
        rightEye = [coords[i] for i in RIGHT_EYE_IDX]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EAR_THRESHOLD:
            self.counter += 1
        else:
            if self.counter >= CONSEC_FRAMES:
                self.blinks += 1
                self.counter = 0
                return True
            self.counter = 0
        return False


# attendance_system/ai_modules/liveness_detection.py NEW CODE FOR VIDEO IDENTIFY
# import cv2
# import numpy as np
# import dlib
# from scipy.spatial import distance as dist
# import torch
# import torchvision.transforms as transforms

# # Path to model
# SHAPE_PREDICTOR_PATH = r"c:\Users\viraj\Downloads\attendance_system\attendance_system\models\shape_predictor_68_face_landmarks.dat"



# detector = dlib.get_frontal_face_detector()
# predictor = None
# try:
#     predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
# except Exception as e:
#     print("dlib predictor not found; liveness detection won't work:", e)

# # Eye aspect ratio helper
# def eye_aspect_ratio(eye):
#     A = dist.euclidean(eye[1], eye[5])
#     B = dist.euclidean(eye[2], eye[4])
#     C = dist.euclidean(eye[0], eye[3])
#     eps = 1e-6
#     return (A + B) / (2.0 * (C + eps))

# # Indexes for 68-landmark model
# LEFT_EYE_IDX = list(range(36, 42))
# RIGHT_EYE_IDX = list(range(42, 48))

# # Blink detection thresholds
# EAR_THRESHOLD = 0.22
# CONSEC_FRAMES = 2

# class BlinkDetector:
#     """ Simple blink detector for compatibility """
#     def __init__(self):
#         self.counter = 0
#         self.blinks = 0

#     def process(self, gray_frame, rect):
#         if predictor is None:
#             return False
#         if isinstance(rect, tuple):
#             top, right, bottom, left = rect
#             rect_dlib = dlib.rectangle(left, top, right, bottom)
#         else:
#             rect_dlib = rect

#         shape = predictor(gray_frame, rect_dlib)
#         coords = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
#         leftEye = [coords[i] for i in LEFT_EYE_IDX]
#         rightEye = [coords[i] for i in RIGHT_EYE_IDX]
#         leftEAR = eye_aspect_ratio(leftEye)
#         rightEAR = eye_aspect_ratio(rightEye)
#         ear = (leftEAR + rightEAR) / 2.0

#         if ear < EAR_THRESHOLD:
#             self.counter += 1
#         else:
#             if self.counter >= CONSEC_FRAMES:
#                 self.blinks += 1
#                 self.counter = 0
#                 return True
#             self.counter = 0
#         return False
    
# class DepthLivenessDetector:
#     def __init__(self, model_type="DPT_Hybrid"):
#         """
#         Depth-based liveness detector using MiDaS.
#         model_type can be 'DPT_Large', 'DPT_Hybrid', or 'MiDaS_small'
#         """
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#         # Load MiDaS model from torch hub
#         self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
#         self.midas.to(self.device)
#         self.midas.eval()

#         # Load transforms
#         self.transform = torch.hub.load("intel-isl/MiDaS", "transforms")
#         if model_type in ["DPT_Large", "DPT_Hybrid"]:
#             self.transform = self.transform.dpt_transform
#         else:
#             self.transform = self.transform.small_transform

#     def check_depth_variance(self, frame, face_location, threshold=0.02):
#         """
#         Check if the face ROI has enough depth variance (to avoid flat screens).
#         - face_location: (top, right, bottom, left)
#         - threshold: minimum variance to consider as real
#         Returns: True if liveness confirmed, False otherwise
#         """
#         top, right, bottom, left = face_location
#         face_roi = frame[top:bottom, left:right]

#         if face_roi.size == 0:
#             return False

#         # Preprocess
#         input_batch = self.transform(face_roi).to(self.device)

#         with torch.no_grad():
#             prediction = self.midas(input_batch)

#             # Resize to original face ROI
#             prediction = torch.nn.functional.interpolate(
#                 prediction.unsqueeze(1),
#                 size=face_roi.shape[:2],
#                 mode="bicubic",
#                 align_corners=False,
#             ).squeeze()

#         depth_map = prediction.cpu().numpy()

#         # Normalize
#         depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min() + 1e-6)

#         # Calculate variance
#         variance = np.var(depth_map)

#         print(f"[DepthLiveness] Variance={variance:.4f}")

#         return variance > threshold

# class LivenessDetector:
#     """ Combines blink + head movement """
#     def __init__(self):
#         self.blink_detector = BlinkDetector()
#         self.last_nose_x = None
#         self.last_nose_y = None

#     def process(self, gray_frame, rect):
#         if predictor is None:
#             return False

#         if isinstance(rect, tuple):
#             top, right, bottom, left = rect
#             rect_dlib = dlib.rectangle(left, top, right, bottom)
#         else:
#             rect_dlib = rect

#         shape = predictor(gray_frame, rect_dlib)
#         coords = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

#         # --- Blink Check ---
#         blinked = self.blink_detector.process(gray_frame, rect_dlib)

#         # --- Head Movement Check ---
#         nose = coords[30]  # Nose tip
#         movement_detected = False
#         if self.last_nose_x is not None:
#             dx = abs(nose[0] - self.last_nose_x)
#             dy = abs(nose[1] - self.last_nose_y)
#             if dx > 2 or dy > 2:  # small natural movement
#                 movement_detected = True
#         self.last_nose_x, self.last_nose_y = nose

#         # Must blink + move head slightly
#         return blinked and movement_detected
    

