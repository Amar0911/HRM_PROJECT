from django.contrib import admin
from .models import  Leave, LeaveQuota

# Register your models here.


admin.site.register(Leave)
admin.site.register(LeaveQuota)
