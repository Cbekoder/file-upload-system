from .models import Script
from modeltranslation.translator import TranslationOptions, register

@register(Script)
class ScriptTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')