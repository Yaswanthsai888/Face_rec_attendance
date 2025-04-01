import os
import pickle
import logging
import numpy as np
import cv2
import dlib
import imutils

import tkinter as tk
from tkinter import messagebox
import face_recognition

def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button

def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt

def msg_box(title, description):
    messagebox.showinfo(title, description)

def detect_eye_blink(frame):
    """
    Detect eye blink using facial landmarks.
    
    Args:
        frame (numpy.ndarray): Input image frame
    
    Returns:
        bool: True if blink detected, False otherwise
    """
    # Initialize dlib's face detector and facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = detector(gray)
    
    for face in faces:
        # Detect facial landmarks
        landmarks = predictor(gray, face)
        
        # Extract left and right eye coordinates
        left_eye_points = []
        right_eye_points = []
        
        # Landmark indices for eyes (based on dlib 68-point model)
        left_eye_indices = list(range(36, 42))
        right_eye_indices = list(range(42, 48))
        
        for n in left_eye_indices:
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            left_eye_points.append((x, y))
        
        for n in right_eye_indices:
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            right_eye_points.append((x, y))
        
        # Calculate eye aspect ratio (EAR)
        def eye_aspect_ratio(eye_points):
            # Vertical eye landmarks
            A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
            B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
            
            # Horizontal eye landmark
            C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
            
            # EAR
            ear = (A + B) / (2.0 * C)
            return ear
        
        left_ear = eye_aspect_ratio(left_eye_points)
        right_ear = eye_aspect_ratio(right_eye_points)
        
        # Average EAR
        avg_ear = (left_ear + right_ear) / 2.0
        
        # Blink threshold (adjust as needed)
        EAR_THRESHOLD = 0.2
        
        # Blink detection
        if avg_ear < EAR_THRESHOLD:
            return True
    
    return False

def recognize(img, db_path, tolerance=0.6):
    """
    Improved face recognition with better matching and logging.
    
    Args:
        img (numpy.ndarray): Input image
        db_path (str): Path to face encodings database
        tolerance (float): Face matching tolerance (lower is stricter)
    
    Returns:
        str: Name of recognized person or status
    """
    try:
        # Detect face encodings
        embeddings_unknown = face_recognition.face_encodings(img)
        
        if len(embeddings_unknown) == 0:
            logging.warning("No faces found in the image")
            return 'no_persons_found'
        
        # Use the first detected face
        embeddings_unknown = embeddings_unknown[0]
        
        # Collect all known face encodings
        known_names = []
        known_encodings = []
        
        for filename in os.listdir(db_path):
            if filename.endswith('.pkl'):
                try:
                    with open(os.path.join(db_path, filename), 'rb') as f:
                        encoding = pickle.load(f)
                        known_encodings.append(encoding)
                        known_names.append(filename[:-4])  # Remove .pkl extension
                except Exception as e:
                    logging.error(f"Error loading encoding {filename}: {e}")
        
        # Compare faces
        if not known_encodings:
            logging.warning("No known faces in database")
            return 'unknown_person'
        
        # Use face_recognition's compare_faces with tolerance
        matches = face_recognition.compare_faces(
            known_encodings, embeddings_unknown, tolerance=tolerance
        )
        
        # Find best match
        face_distances = face_recognition.face_distance(
            known_encodings, embeddings_unknown
        )
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_names[best_match_index]
            logging.info(f"Recognized: {name}")
            return name
        
        logging.warning("No close face match found")
        return 'unknown_person'
    
    except Exception as e:
        logging.error(f"Face recognition error: {e}")
        return 'unknown_person'
