from django.urls import path , include
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register', views.RegisterUserView, basename='register')
urlpatterns = [
    path('', include(router.urls)),
    # Authentication URLs
    path('login/', views.LoginUser.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('MakeFaceEmbedded/' , views.CreateFaceEmbeddedView.as_view() , name = "CreateFace"),
    path('loginFaceEmbedded/' , views.LoginFaceEmbeddedView.as_view() , name = "CreateFace"),
    
]