from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path():
    pass
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='photos')
    fname=models.TextField()
    lname=models.TextField()
    email=models.EmailField(max_length=254)
    def __str__(self):
        return f"Profile of {self.user.username}"
    


class Image(models.Model):
    user_profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='user_images')

class check(models.Model):
    photo=models.ImageField(upload_to='Logs')
    
    

    