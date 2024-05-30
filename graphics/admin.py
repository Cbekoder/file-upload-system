from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Category)
admin.site.register(File)
admin.site.register(RecievedFiles)
admin.site.unregister(Group)

