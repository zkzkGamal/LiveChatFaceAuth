from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request , 'index.html')

def index_auth(request):
    return render(request , 'preform_auth.html')