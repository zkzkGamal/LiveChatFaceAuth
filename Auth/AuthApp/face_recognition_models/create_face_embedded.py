import face_recognition
import cv2
from .handle_image import HandleImage
import numpy as np

class CreateFaceEmbedded:
    """
    _summary_
    Args:
        image (_requested image): take the image from the request or form
    returns:
        face embedding array to save it in the db for later use
    """
    
    def __init__(self):
        self.image = None
        self.img_size = (512 , 512)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.image_handler = HandleImage()
    
    def __call__(self , *args):
        """
        Args:
            *args (_requested image): take the image from the request or form

        Returns:
            face embedding array to save it in the db for later use
        """
        self.image = args[0]
        self.image = self.image_handler(self.image)
        face_locations = self.__get_face_locations_using_face_recognition()
        if face_locations is None:
            face_locations = self.__get_face_using_hera()
        face_encodings = self.__get_face_encodings()
        return face_encodings
    
    def __get_face_locations_using_face_recognition(self):
        """
        Args:
            None

        Returns:
            cropped face array after using face_recognition to detect face location
        """
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        if len(face_locations) == 0 or len(face_locations) > 1:
            return None
        top, right, bottom, left = face_locations[0]
        cropped_face = self.image[top-20:bottom+5, left-10:right+5]
        return cropped_face
    
    def __get_face_using_hera(self):
        """
        _summary_
        Args:
            None

        Returns:
            cropped face array after using Haar cascade to detect face location
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5 , flags=2)
        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cropped_face = self.image[y:y+h, x:x+w]
            break 
        return cropped_face
   
    def __get_face_encodings(self):
        """
        _summary_
        Args:
            None

        Returns:
            face encoding array from face_recognition to save it in the db for later use
        """
        face_encodings = face_recognition.face_encodings(self.image)
        return face_encodings
        
        