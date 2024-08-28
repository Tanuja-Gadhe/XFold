from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from home import views
urlpatterns = [
    path('',views.frontpage,name="frontpage"),
    path('home',views.index,name='home'),
    path('login',views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('register',views.registeruser,name='register'),
    path('profile',views.update_profile,name='profile'),
    path('face_recog',views.face_recog,name='face_recog'),
    path('delete_image/<str:pk>/',views.delete_image,name='delete_image'),
    path('download_image/<str:pk>/',views.download_image,name='download_image'),
    path('view_profile',views.view_profile,name='view_profile'),
   
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATICFILES_DIRS)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)