import face_recognition as fr
import numpy as np
from accounts.models import StudentProfile
from .models import Course
from django.shortcuts import get_object_or_404


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def get_encoded_faces(course_id):
    """
    This function loads all user 
    profile images and encodes their faces
    """
    
    # Create a dictionary to hold the encoded face for each user
    encoded = {}
    
    # get all the students enrolled in the course
    course = get_object_or_404(Course, id=course_id)
    
    # Retrieve all user profiles from the database
    students = course.students.all()
    
    for student in students:
        # Get the encoding and username directly from the profile
        student_profile = student.studentprofile
        full_name = f"{student.first_name} {student.last_name}"
        encoding_str = student_profile.encoding
        if encoding_str:
            encoding = np.fromstring(encoding_str, dtype=float, sep=',')
            encoded[full_name] = encoding
            
        else:
            print(f"No encoding found for user {full_name}")
        
    # Return the dictionary of encoded faces
    return encoded


def classify_face(img, course_id):
    """
    This function takes an image as input and returns the name of the face it contains
    """
    # Load all the known faces and their encodings
    faces = get_encoded_faces(course_id=course_id)
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    # Load the input image
    img = fr.load_image_file(img)
 
    try:
        # Find the locations of all faces in the input image
        face_locations = fr.face_locations(img)

        # Encode the faces in the input image
        unknown_face_encodings = fr.face_encodings(img, face_locations)

        # Identify the faces in the input image
        face_names = []
        for face_encoding in unknown_face_encodings:
            # Compare the encoding of the current face to the encodings of all known faces
            matches = fr.compare_faces(faces_encoded, face_encoding)

            # Find the known face with the closest encoding to the current face
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            # If the closest known face is a match for the current face, label the face with the known name
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        # Return the name of the first face in the input image
        return face_names[0]
    except:
        # If no faces are found in the input image or an error occurs, return False
        return False