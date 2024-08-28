from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .form import ProfileUpdate
from .form import ImageUploadForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import Image
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import base64
import cv2
import os
import face_recognition
import matplotlib.pyplot as plt
from .models import Profile,Image
from django.core.files.base import ContentFile

def frontpage(request):
    return render(request,'frontpage.html')

def loginuser(request):
    if request.method == "POST":
         username = request.POST.get("username")
         password = request.POST.get("password")
         user = authenticate(request, username=username, password=password)
         if user is not None:
            login(request, user)
            return redirect('face_recog')
         else:
            messages.success(request,("There was a error Logging In, Try again"))
            return redirect('login')
    else:
        return render(request,'login.html')
    


@login_required
def face_recog(request):
    profile = Profile.objects.get(user=request.user.id)
    img1_path=profile.photo.path
    print(img1_path)
    img1=face_recognition.load_image_file(img1_path)
    face_location=face_recognition.face_locations(img1)
    face_encoding=face_recognition.face_encodings(img1,face_location)[0]
    match=False
    video_capture = cv2.VideoCapture(0)
    i=0
    while i<=15:
        match=False
        i+=1
        ret,frame = video_capture.read()
        if ret:
            face_location1=face_recognition.face_locations(frame)
    
            if len(face_location1)>0&len(face_location1)<2:
                face_encoding1=face_recognition.face_encodings(frame,face_location1)[0]
                result=face_recognition.compare_faces([face_encoding],face_encoding1)
                if result[0]:
                    match=True
                
                else:
                    match=False
                if cv2.waitKey(1)&0xFF==ord("q"):
                    break
                for (x,y,w,h) in face_location1:
                    cv2.rectangle(frame,(h,x),(y,w),(0,255,0),4)
            
            if match:
                cv2.putText(frame,"matched",(h+6,w-6),cv2.FONT_HERSHEY_COMPLEX,1.0,(255,255,255),1)
                #break
            cv2.imshow("img",frame)
    video_capture.release()
    cv2.destroyAllWindows()
    if match:
        messages.success(request,("Face matched"))
        return redirect('home')
    else:
        messages.success(request,("Face is not recognized, Try again"))
        return redirect('login')
            
        

@login_required
def logoutuser(request):
    return render(request,'frontpage.html')


def registeruser(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You are registered successfully"))
            return redirect('profile')

    else:
        form=UserCreationForm()

    return render(request,'register.html',{
        'form':form,
    })

@login_required
def update_profile(request):
    if request.method=="POST":
        current=User.objects.get(id=request.user.id)
        p_form=ProfileUpdate(request.POST,request.FILES,instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            login(request,current)
            messages.success(request,("You are Profile has been created successfully"))
            return redirect('home')
        else:
            messages.success(request,("There was an error"))
            return render(request,'profile.html')
        
    else:
        p_form=ProfileUpdate()
        context={'p_form':p_form}
        return render(request,'profile.html',context)

@login_required
def index(request):
    if request.method=='POST':
        form=ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user_profile=request.user.profile
            image.save()
    form=ImageUploadForm()
    img=Image.objects.filter(user_profile=request.user.profile)
    return render(request,'index.html',{'img':img,'form':form})

@login_required
def delete_image(request,pk):
    instance = get_object_or_404(Image, pk=pk)
    instance.image.delete()  
    instance.delete()  
    return redirect('home')


@login_required
def download_image(request,pk):
    instance = get_object_or_404(Image, pk=pk)
    image_data = open(instance.image.path, 'rb').read()
    response = HttpResponse(image_data, content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{instance.image.name}"'
    return response

@login_required
def view_profile(request):
    user_profile = request.user.profile
    return render(request, 'view_profile.html', {'user_profile': user_profile})
