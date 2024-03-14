from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

@admin.register(Script)
class ScriptAdmin(TranslationAdmin):
    list_display = ('id', 'question', 'answer')

admin.site.register(NodeGroups)

# @admin.register(Folder)
# class FolderAdmin(TranslationAdmin):
#     list_display = ('id', 'title', 'user_id.firstname')