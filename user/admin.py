
from django.contrib import admin

# Register your models here.
# from .models import UserProfile
from .models import UserProfile

class BaseSetting(admin.ModelAdmin):
    list_display = ['username','email']


admin.site.register(UserProfile,BaseSetting)
