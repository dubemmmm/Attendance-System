import face_recognition
import cv2
import csv
import numpy as np
import os
from django.core.cache import cache

from datetime import datetime
from PIL import Image
from django.shortcuts import get_object_or_404, redirect
face_encoder = face_recognition.api.face_encodings


# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendace_system.settings')
import django
django.setup()

from accounts.models import StudentProfile
from attendace.models import Course







def take_attendance(img_names, img_encodings):
    face_locations = []
    face_encodings = []
    face_names = []
    s = True
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    # Initialize the camera
    video_capture = cv2.VideoCapture(0)

    # Load known face encodings and names
    # Assuming known_face_encoding and known_faces_names are defined somewhere

    # Open CSV file for writing attendance data 
    current_date = datetime.now().strftime('%Y-%m-%d')
    csv_filename = current_date + '.csv'

# Read existing entries into a set
    existing_entries = set()
    try:
        with open(csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                existing_entries.add(row[0])
    except FileNotFoundError:
        pass

    with open(csv_filename, 'a', newline='') as csvfile:
        lnwriter = csv.writer(csvfile)

        # Main loop for real-time face recognition
        while True:
            # Capture a frame from the camera
            ret, frame = video_capture.read()
        
            # Convert the frame from BGR to RGB (required for face_recognition library)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
            # Find all face locations and encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
            # Loop through each face found in the frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare the face encoding with known face encodings
                matches = face_recognition.compare_faces(img_encodings, face_encoding)
                name = "Unknown"  # Default name if face is not recognized
            
                # Check if any known face matches the current face
                if True in matches:
                    first_match_index = matches.index(True)
                    name = img_names[first_match_index]
            
                # Write attendance data to CSV if the name is not already present
                if name != 'Unknown' and name not in existing_entries:
                    current_time = datetime.now().strftime('%H:%M:%S')
                    lnwriter.writerow([name, current_time, 'present'])
                    existing_entries.add(name)  # Add the name to the set
            
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
            # Display the frame with recognized faces
            cv2.imshow('Attendance System', frame)
        
            # Check for user input to quit the loop (press 'q' to exit)
            if cv2.waitKey(1000) & 0xFF == ord('q'):
                break

    # Release the camera and close all windows
    video_capture.release()
    cv2.destroyAllWindows()
    
def main():
    print('running the predict script...')

    img_names = []
    img_encodings = []
    course = get_object_or_404(Course, id=1)
    print('the course title is ', course.course_title)
    students = course.students.all()
    for student in students:
        student_profile = student.studentprofile
        full_name = f"{student.first_name} {student.last_name}"
        print(full_name)
        encoding_array = np.fromstring(student_profile.encoding, dtype=float, sep=',')
        img_encodings.append(encoding_array)
        img_names.append(full_name)
    #take_attendance(img_names, img_encodings)
    #print(img_names)
    #print(img_encodings)
if __name__ == '__main__':
    main()
    

