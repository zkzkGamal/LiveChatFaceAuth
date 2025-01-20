from rest_framework import serializers 
import requests
from PIL import Image , UnidentifiedImageError
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def custom_error_message(error):
    """
    Processes an error dictionary to convert specific string values into their 
    appropriate types (e.g., 'True'/'False' to boolean, status codes to integers).

    Args:
        error (dict): A dictionary containing error details, expected to have a 
                      'non_field_errors' key with a list of error items.

    Returns:
        dict: The processed error data with converted boolean and integer values 
              or a generic error message if an exception occurs.
    """
    try:
        print(error)
        error_data = error.get('non_field_errors')[0]
        for key , v  in error_data.items():
            if key == 'success':
                if v == 'True':
                    error_data[key] = True
                elif v == "False":
                    error_data[key] = False
            if key == 'status_code':
                if v in ['200','400','500']:
                    error_data[key] = int(v)
        return error_data
    except Exception as e:
        return {'status_code':400 ,'message': f"failed to retrieve data please see this error : {error}" , 'data':{}}


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(allow_null = True)
    
    def validate(self, attrs):
        """
        Validates the image in the serializer.

        Args:
            attrs (dict): The deserialized data from the request.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If no image is uploaded or if the image is
                not valid.
        """
        image = attrs.get('image')
        if image is None:
            raise serializers.ValidationError([{'status_code': 400, 'message': "no images uploaded", 'data': {}}])
        try:
            image = Image.open(image)
            image.verify()
        except UnidentifiedImageError:
            raise serializers.ValidationError([{'status_code': 400, 'message': "image is not valid", 'data': {}}])
        except (IOError, ValidationError):
            raise serializers.ValidationError([{'status_code': 400, 'message': "image is not valid", 'data': {}}])
        return attrs
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username' , 'id',)
    
class MyTokenSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user'] = UserSerializer(user).data
        try:
            token['profile_id'] = user.profile.pk
        except:
            token['profile_id'] = None
        return token

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'password' , )
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not username:
            raise serializers.ValidationError({'message': 'Username is required'}, code='invalid')
        if not password:
            raise serializers.ValidationError({'message': 'Password is required'}, code='invalid')

        if username.isdigit() or len(username) < 2 or len(username) > 20:
            raise serializers.ValidationError({'message': 'Username can not contain only numbers'}, code='invalid')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'message': 'this username is taken'}, code='invalid')

        if password.isdigit() or len(password) < 8 or len(password) > 20:
            raise serializers.ValidationError({'message': 'Password must be at least 8 characters'}, code='invalid')
        if password == username:
            raise serializers.ValidationError({'message': 'Password must be different from username'}, code='invalid')
        return [attrs , True]
    
