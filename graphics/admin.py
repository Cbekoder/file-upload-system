from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

admin.site.register(Category)
admin.site.register(File)
admin.site.register(RecievedFiles)