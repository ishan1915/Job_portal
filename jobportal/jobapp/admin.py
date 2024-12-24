from django.contrib import admin
from .models import UserDetail,Skill,Resume

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Skill)
admin.site.register(Resume)