from django.contrib import admin
from .models import UserDetail,Skill,Resume,Education,Certification,Job,Application,ContactUs,Company

# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Skill)
admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(Certification)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(ContactUs)
admin.site.register(Company)