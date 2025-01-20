from PIL import Image
import cv2
import numpy as np

class HandleImage:
    """
    _summary_
    this class used to handle request image and process it to face_recognition model
    how to use:\n
        image = HandleImage()
        image(request.data.get("image"))
    Args:
        image  (requested image): get the image from request in api or form and handle it
    returns:
        cv2 image to process in face_recognition model
    
    """
    def __init__(self):
        self.image = None
        self.img_size = (512 , 512)
    
    def __call__(self, *args):
        """_summary_
        Args:
            image  (requested image): get the image from request in api or form and handle it
        returns:
            cv2 image to process in face_recognition model
        """
        self.image = args[0]
        return self.__process_image(self.image)
    
    def __process_image(self , image):
        """_summary_

        Args:
            image (_type_): request image

        Returns:
            cv2 image
        """
        img = Image.open(image)
        img = np.array(img)
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        img = cv2.resize(img , self.img_size)
        return img
        