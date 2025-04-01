import numpy
import util
import os
import os.path
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import datetime
import logging
import face_recognition
import pickle

# Configure logging
logging.basicConfig(filename='attendance.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition Attendance System")
        self.main_window.geometry("1200x620+350+100")
        self.main_window.configure(bg='#f0f0f0')

        # Camera selection
        self.camera_index = self._find_camera()
        if self.camera_index is None:
            messagebox.showerror("Error", "No camera found!")
            self.main_window.quit()
            return

        # UI Elements
        self._create_ui_elements()

        # Directories
        self.db_dir = './images1'
        self.log_path = './Attendance.csv'
        os.makedirs(self.db_dir, exist_ok=True)

        # Logging setup
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w') as f:
                f.write("Timestamp,Name,Registration Number\n")

        # Blink detection variables
        self.blink_required = True
        self.blink_detected = False
        self.blink_attempts = 0
        self.MAX_BLINK_ATTEMPTS = 3

    def _find_camera(self):
        """Find the first available camera."""
        for i in range(3):  # Try first 3 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.release()
                return i
        return None

    def _create_ui_elements(self):
        # Webcam display
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=10, width=700, height=500)

        # Buttons with improved styling
        button_frame = tk.Frame(self.main_window, bg='#f0f0f0')
        button_frame.place(x=750, y=250)

        self.login_button = util.get_button(
            button_frame, 'Login', '#4CAF50', self.login, fg='white'
        )
        self.login_button.pack(pady=10)

        self.register_button = util.get_button(
            button_frame, 'Register New User', '#2196F3', self.register_new_user, fg='white'
        )
        self.register_button.pack(pady=10)

        # Status and blink instruction label
        self.status_label = tk.Label(
            self.main_window, text="", bg='#f0f0f0', 
            font=('Arial', 12), wraplength=300
        )
        self.status_label.place(x=750, y=450)

        self.add_webcam(self.webcam_label)

    def add_webcam(self, label):
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise IOError("Cannot open webcam")
            
            self._label = label
            self.process_webcam()
        except Exception as e:
            logging.error(f"Webcam error: {e}")
            messagebox.showerror("Camera Error", str(e))

    def process_webcam(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                raise IOError("Failed to capture frame")

            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

            self._label.after(20, self.process_webcam)
        except Exception as e:
            logging.error(f"Webcam processing error: {e}")
            self.status_label.config(text=f"Camera error: {e}", fg='red')

    def login(self):
        try:
            # Capture and save temporary image
            temp_img_path = os.path.join(self.db_dir, 'temp_login.jpg')
            cv2.imwrite(temp_img_path, self.most_recent_capture_arr)

            # Blink detection for anti-spoofing
            if self.blink_required:
                # Detect eye blink
                blink_detected = util.detect_eye_blink(self.most_recent_capture_arr)
                
                if not blink_detected:
                    self.blink_attempts += 1
                    
                    if self.blink_attempts >= self.MAX_BLINK_ATTEMPTS:
                        self.status_label.config(
                            text="Multiple failed blink attempts. Possible spoofing detected!", 
                            fg='red'
                        )
                        logging.warning("Potential spoofing attempt detected")
                        return
                    
                    self.status_label.config(
                        text=f"Please blink to verify. Attempt {self.blink_attempts}/{self.MAX_BLINK_ATTEMPTS}", 
                        fg='orange'
                    )
                    return
                
                # Reset blink tracking
                self.blink_attempts = 0
                self.blink_detected = True

            # Recognize face
            result = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if result == 'no_persons_found':
                self.status_label.config(text="No face detected", fg='red')
                logging.warning("Login attempt: No face detected")
            elif result == 'unknown_person':
                self.status_label.config(text="Unknown person", fg='orange')
                logging.info("Login attempt: Unknown person")
            else:
                # Successful recognition
                name = result
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Log attendance
                with open(self.log_path, 'a') as f:
                    f.write(f"{timestamp},{name},Attended\n")
                
                self.status_label.config(text=f"Welcome, {name}!", fg='green')
                logging.info(f"Successful login: {name}")

            # Clean up temporary image
            os.remove(temp_img_path)

        except Exception as e:
            logging.error(f"Login error: {e}")
            self.status_label.config(text=f"Login error: {e}", fg='red')

    def register_new_user(self):
        try:
            # Open registration dialog
            name = simpledialog.askstring("Registration", "Enter your name:")
            if not name:
                return

            reg_no = simpledialog.askstring("Registration", "Enter registration number:")
            if not reg_no:
                return

            # Capture registration image
            temp_reg_path = os.path.join(self.db_dir, f'{name}_{reg_no}.jpg')
            cv2.imwrite(temp_reg_path, self.most_recent_capture_arr)

            # Compute face encodings
            face_encodings = face_recognition.face_encodings(
                face_recognition.load_image_file(temp_reg_path)
            )

            if not face_encodings:
                os.remove(temp_reg_path)
                messagebox.showerror("Error", "No face detected in the image")
                return

            # Save face encoding
            encoding_path = os.path.join(self.db_dir, f'{name}_{reg_no}.pkl')
            with open(encoding_path, 'wb') as f:
                pickle.dump(face_encodings[0], f)

            messagebox.showinfo("Success", f"User {name} registered successfully!")
            logging.info(f"User registered: {name} ({reg_no})")

        except Exception as e:
            logging.error(f"Registration error: {e}")
            messagebox.showerror("Error", str(e))

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
