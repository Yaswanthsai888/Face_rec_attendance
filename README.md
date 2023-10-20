# Face_rec_attendance.

It's a simple face recognition application with a graphical user interface built using Tkinter. Here's a step-by-step explanation of how the code functions:

Import Libraries:

The code begins by importing necessary libraries such as util (which appears to be a custom utility module), os.path, subprocess, tkinter for creating the GUI, cv2 for handling video capture, and PIL for image manipulation.
Initialize the Application:

The App class is defined, which represents the main application window.
The main window is created using Tkinter, and its dimensions are set.
Create UI Elements:

Three buttons are created using a custom util function: "login," "register new user," and "Try again."
Webcam Display:

An area for displaying the webcam feed is set up using an image label.
The webcam feed is captured using the OpenCV (cv2) library and displayed in the GUI.
Face Recognition and Login:

The "login" button is associated with the login method. When clicked, this method performs the following steps:
Captures the current frame from the webcam and saves it as a temporary image (unknown_img_path).
Runs the face recognition process on the temporary image using subprocess to execute the face_recognition script.
Extracts the name of the recognized person from the output.
Displays a message box welcoming the recognized user or indicating that the user is unknown.
Logs the attendance record (name and "Attendance") in a text file (log_path).
Deletes the temporary image.
User Registration:

The "register new user" button is associated with the register_new_user method. When clicked, this method opens a new window where a user can input their username and registration number (reg_no).
The user's image is captured and displayed.
When the "Accept" button is clicked, the user's name and registration number are extracted, and the user's image is saved in the db_dir.
A success message is displayed, and the registration window is closed.
Additional Functionality:

The code uses custom utility functions from the util module for creating buttons, labels, and text input fields.
Running the Application:

The start method is called to start the main application window.
Main Entry Point:

The code checks if it's being run as the main script, and if so, it creates an instance of the App class and starts the GUI application.
In summary, this code creates a simple face recognition application with a GUI. Users can log in, and new users can be registered by capturing their images and inputting their details. Attendance records are saved in a text file. The application captures the webcam feed and uses the Dlib-based face_recognition library to recognize faces. Detected faces are associated with user names for login and registration.
