from django.shortcuts import render , redirect
from django.http import JsonResponse
import numpy as np
from rest_framework import generics , response , status , viewsets
from . import serializers
from django.urls import reverse
from AuthApp.face_recognition_models.create_face_embedded import CreateFaceEmbedded
from . import models
import json
embedder = CreateFaceEmbedded()
# Create your views here.
def index(request):
    return JsonResponse({'message': 'hello world'} , safe=False)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class RegisterUserView(viewsets.ViewSet):
    serializer_class = serializers.UserRegisterSerializer
    def create(self , request):
        # create user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # get the tokens for the user
            refresh = self.create_custom_claims(user ,RefreshToken.for_user(user))
            access_token = self.create_custom_claims(user , refresh.access_token)
            active_face_recognition = reverse("CreateFace")
            # put the user data 
            response_data = {
                "status_code":200,
                "message":"success",
                "data":{
                    'refresh': str(refresh),
                    'access': str(access_token),
                    "active_face_recognition":active_face_recognition
                }
            }
            return response.Response(response_data , status= status.HTTP_201_CREATED)
        return response.Response(serializers.custom_error_message(serializer.errors) , status=status.HTTP_200_OK)
    # to make custem token for registerd user
    def create_custom_claims(self, user , token):
        token['user'] = {
            'user_id':user.id,
            'username':user.username
        }
        try:
            token['profile_id'] = user.userprofile.pk
        except:
            token['profile_id'] = None
        try:    
            token['photo'] = str(user.userprofile.photo)
        except:
            token['photo'] = ""
        return token
        
class LoginUser(TokenObtainPairView, generics.GenericAPIView):
    serializer_class = serializers.MyTokenSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            
            if serializer.is_valid():
                    response_data =  super().post(request, *args, **kwargs)
                    return response.Response({
                        'status_code':200 , "message":"success",
                        "data":response_data.data
                    })
            
            else:return response.Response(serializers.custom_error_message(serializer.errors) , status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
                return response.Response({
                    'status_code':400 , "message":"No active account found with the given credentials",
                })



class CreateFaceEmbeddedView(generics.GenericAPIView):
    serializer_class = serializers.ImageSerializer
    
    def post(self , request , *args , **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            embedder_user , code = embedder(self.request.data['image'])
            if code == 400:
                return response.Response({
                    'status_code':400 , "message":embedder_user,
                })
            embedder_user = np.array(embedder_user).tolist()
            emb_user , _ = models.UserEmbeddedImage.objects.get_or_create(embedded_image = embedder_user)
            return response.Response(
                {"a":embedder_user}
            )
        else:return response.Response(
            serializers.custom_error_message(serializer.errors)
        )