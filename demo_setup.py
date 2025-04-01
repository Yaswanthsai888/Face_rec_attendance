import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
import face_recognition
import pickle

class DemoSetup:
    def __init__(self):
        self.demo_dir = './demo_users'
        os.makedirs(self.demo_dir, exist_ok=True)
        
        self.demo_users = [
            {"name": "John Doe", "reg_no": "CS2021001"},
            {"name": "Jane Smith", "reg_no": "EE2021002"},
            {"name": "Mike Johnson", "reg_no": "ME2021003"}
        ]
    
    def create_demo_users(self):
        """Create demo user profiles with sample images."""
        print("🚀 Setting up demo users...")
        
        # Simulating face capture and encoding
        for user in self.demo_users:
            # In a real scenario, you'd capture actual face images
            # Here we'll simulate with a placeholder
            demo_image_path = self._generate_demo_image(user['name'])
            
            if demo_image_path:
                face_encodings = face_recognition.face_encodings(
                    face_recognition.load_image_file(demo_image_path)
                )
                
                if face_encodings:
                    encoding_path = os.path.join(
                        self.demo_dir, 
                        f"{user['name']}_{user['reg_no']}.pkl"
                    )
                    with open(encoding_path, 'wb') as f:
                        pickle.dump(face_encodings[0], f)
                    
                    print(f"✅ Created demo profile for {user['name']}")
    
    def _generate_demo_image(self, name):
        """Generate a placeholder demo image."""
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a blank image
        img = Image.new('RGB', (400, 400), color='white')
        d = ImageDraw.Draw(img)
        
        # Use a font
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()
        
        # Draw name
        d.text((50,50), name, fill=(0,0,0), font=font)
        
        # Save image
        img_path = os.path.join(self.demo_dir, f"{name}_demo.jpg")
        img.save(img_path)
        
        return img_path
    
    def launch_demo_video(self):
        """Launch a simulated demo video explaining the system."""
        print("🎥 Launching Demo Video...")
        messagebox.showinfo(
            "Face Recognition Attendance Demo", 
            "Welcome to the Face Recognition Attendance System Demo!\n\n"
            "This demo will showcase:\n"
            "1. User Registration\n"
            "2. Face Recognition Login\n"
            "3. Attendance Tracking\n\n"
            "Please check the console for more details."
        )
    
    def run_demo(self):
        self.create_demo_users()
        self.launch_demo_video()
        
        print("\n🌟 Demo Setup Complete!")
        print("Next steps:")
        print("1. Run facemain.py to start the application")
        print("2. Use demo users to test registration and login")

def main():
    demo = DemoSetup()
    demo.run_demo()

if __name__ == "__main__":
    main()
