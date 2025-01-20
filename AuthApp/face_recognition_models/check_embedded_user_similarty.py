import os
from AuthApp import models
import numpy as np
import faiss
from .create_face_embedded import CreateFaceEmbedded
import logging
logger = logging.Logger(__name__)
all_faces_embedded = models.UserEmbeddedImage.objects.all()

class CheckEmbeddedUserSimilarty:
    def __init__(self):
        
        self.embedder = CreateFaceEmbedded()
        self.all_embedded_faces = all_faces_embedded
        self.all_emdedd_users = all_faces_embedded
        self.image = None
        self.new_embedded_face = None
        self.index = None
        self.index_path = 'AuthApp/face_recognition_models/user_face_embeddings.index'
    
    def __call__(self, *args , **kwg):
        input_type = kwg.get('input_type')
        if input_type == "train":
            self.__process_all_embedded_images()
            self.__train_fAISS_model()
            return 200
        else:
            self.new_embedded_face = args[0]
            if input_type == "register":
                code = self.__write_new_usrs()
                return code
            else:
                user , code = self.__search_similar()
                return user , code
                
    
    def __process_all_embedded_images(self):
        
        stored_embeddings = []
        for user in self.all_embedded_faces:
            embedding = np.array(user.embedded_image, dtype=np.float32)
            stored_embeddings.append(embedding)
        self.all_embedded_faces = np.array(stored_embeddings)
    
    def __train_fAISS_model(self):
        dimension = self.all_embedded_faces.shape[1]  
        index = faiss.IndexFlatL2(dimension)
        index.add(self.all_embedded_faces)
        faiss.write_index(index, self.index_path)
        self.index = index
        return index
    
    def __write_new_usrs(self):
        try:
            new_user_embedding = np.array(self.new_embedded_face, dtype=np.float32).reshape(1, -1)
            try:
                index = faiss.read_index(self.index_path)
            except (FileNotFoundError , Exception):
                # If no index exists, initialize an empty index and add the new user embedding
                index = faiss.IndexFlatL2(new_user_embedding.shape[1])
                index.add(new_user_embedding)
                faiss.write_index(index, self.index_path)
                logger.warning("New FAISS index created and saved with the first user's embedding.")
                return 200
            k = 1 
            distances, indices = index.search(new_user_embedding, k)
            similarity_distance = distances[0][0]
            if similarity_distance < 0.2:
                return 405
            index.add(new_user_embedding)
            logger.warning("the user is being passed to model")
            faiss.write_index(index, self.index_path)
            return 200
        except Exception as e:
            return 400
        
    def __search_similar(self):
        try:
            new_user_embedding = np.array(self.new_embedded_face, dtype=np.float32).reshape(1, -1)
            index = faiss.read_index(self.index_path)
            k = 1 
            distances, indices = index.search(new_user_embedding, k)
            most_similar_user_index = indices[0][0]
            similarity_distance = distances[0][0]
            if similarity_distance < 0.20:      # this mean that the simirality distance is more than 30%
                try:
                    similar_user = models.UserEmbeddedImage.objects.get(pk = most_similar_user_index+1)
                    logger.warning("the user is being getted from the model db")
                    return similar_user.user , 200
                except:
                    similar_user = self.all_emdedd_users[most_similar_user_index]
                    return similar_user.user , 200
            else:
                return None , 400
        except:
            return None , 500

        
        
        