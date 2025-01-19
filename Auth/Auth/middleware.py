from django.http import JsonResponse 
from django.middleware.csrf import CsrfViewMiddleware
import base64
import os
from dotenv import load_dotenv
load_dotenv()


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
    def __call__(self, request):
        key = os.getenv("middleware_key")
        api_key = request.headers.get('X-Key')
        api_key = self.decode_text(api_key)
        if  request.path.startswith('/uploads/') or\
                request.path.endswith('/favicon.ico') :
            return self.get_response(request)
        if not api_key:return self.get_response(request)
        if api_key != key:return self.get_response(request)
        elif api_key == key :return self.get_response(request)