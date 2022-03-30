from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin



# Register your models here.

admin.site.register(Proposal)
admin.site.register(Project)
admin.site.register(Contract)
admin.site.register(Task)
admin.site.register(Document)
# admin.site.register(Users)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Job)

