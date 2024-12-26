from django.contrib import admin
from .models import UserDetail,Skill,Resume,Education,Certification

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Skill)
admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Certification)