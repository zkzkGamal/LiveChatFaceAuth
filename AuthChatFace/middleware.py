from django.http import JsonResponse 
from django.middleware.csrf import CsrfViewMiddleware
import base64
import os
from dotenv import load_dotenv
load_dotenv()
from cryptography.fernet import Fernet
cipher = Fernet(os.getenv("cipher").encode())

class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.csrf_middleware = CsrfViewMiddleware(get_response)
    def decode_text(self , code):
        try:
            askdecode = code.encode()
            text = base64.decodebytes(askdecode).decode("utf-8")
            return text
        except Exception as e:
            return JsonResponse({'error': 'please provide the correct api key to continue'}, status=403)
        
    def decrypt_token(self,text:str):
        try:
            return cipher.decrypt(text.encode()).decode()
        except Exception as e:  
            return 0
        
    def handle_token(self , token):
        if token is not None:
            try:
                type_token , auth_token = token.split(" ")
                token = self.decrypt_token(auth_token)
                if token == 0: return None
                token = type_token + " " + str(token)
                return token
            except Exception as e:
                return JsonResponse({'error': 'please provide the correct auth token to continue'}, status=403)
    def __call__(self, request):
        key = os.getenv("middleware_key")
        api_key = request.headers.get('X-Key')
        token = request.headers.get('authorization')
        if token is None: return self.get_response(request)
        request.META["HTTP_AUTHORIZATION"] = self.handle_token(token)        
        api_key = self.decode_text(api_key)
        if  request.path.startswith('/uploads/') or\
                request.path.endswith('/favicon.ico') :
            return self.get_response(request)
        if not api_key and 'X-CSRFToken' not in request.headers:return self.get_response(request)
        if api_key != key:return self.get_response(request)
        elif api_key == key and  'X-CSRFToken' in request.headers :return self.csrf_middleware(request)  # for web auth 
        elif  api_key == key and  'X-CSRFToken' not in request.headers :return self.get_response(request)  # for mobile auth
        else: return self.get_response(request)

# middlewares.py
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework.exceptions import AuthenticationFailed

@database_sync_to_async
def get_user(token):
    try:
        from rest_framework_simplejwt.authentication import JWTAuthentication
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user
    except AuthenticationFailed:
        return None

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        data = scope.get("subprotocols") if scope.get("subprotocols") else None
        if isinstance(data, list) and len(data) == 4:
            _, token, key, session = data
            user = await get_user(token)
            scope.update({
                'user': user,
                'session': session,
                'key': key
            })
        else:
            scope.update({'user': None, 'session': None, 'key': None})
        
        return await super().__call__(scope, receive, send)
    
    
    
    
