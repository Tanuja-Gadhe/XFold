from django.contrib import admin
from home.models import Profile
from home.models import Image

from home.models import check
# Register your models here.

admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(check)

