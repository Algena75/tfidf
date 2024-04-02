from django.contrib import admin

from .models import File, Word, WordFile

admin.site.register(File)
admin.site.register(Word)
admin.site.register(WordFile)
