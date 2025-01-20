from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics , response , status , viewsets
from . import serializers
# Create your views here.
def index(request):
    return JsonResponse({'message': 'hello world'} , safe=False)

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(viewsets.ViewSet):
    serializer_class = serializers.UserRegisterSerializer
    def create(self , request):
        # create user
        serializer = self.serializer_class(data=request.data)
        if not isinstance(serializer.validate(request.data) , list):
            pass
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            
            # get the tokens for the user
            refresh = self.create_custom_claims(user ,RefreshToken.for_user(user))
            access_token = self.create_custom_claims(user , refresh.access_token)
            # put the user data 
            response_data = {
                'access': str(access_token),
                'refresh': str(refresh),
                'success': True,
            }
            return response.Response(response_data , status= status.HTTP_201_CREATED)
        return response.Response(serializers.custom_error_message(serializer.errors) , status=status.HTTP_400_BAD_REQUEST)
    # to make custem token for registerd user
    def create_custom_claims(self, user , token):
        token['user'] = {
            'user_id':user.id,
            'username':user.username
        }
        try:
            token['profile_id'] = user.profile.pk
        except:
            token['profile_id'] = None
        token['photo'] = str(user.profile.photo)

        if hasattr(user.profile, 'patient'):
                token['patient_id'] = user.profile.patient.pk
        if hasattr(user.profile, 'doctor'):
                token['doctor_id'] = user.profile.doctor.pk
        token['user'] = serializers.Userdataserislizer(user).data

        return token
        
class LoginUser(TokenObtainPairView, generics.GenericAPIView):
    serializer_class = serializers.MyTokenSerializers