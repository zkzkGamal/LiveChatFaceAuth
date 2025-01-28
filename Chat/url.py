from django.urls import path
from . import views
urlpatterns = [
    path('' , views.index),
    path('preform_auth/' , views.index_auth),
]