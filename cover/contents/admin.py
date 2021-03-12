from django.contrib import admin
from .models import Content, Image
# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image

class ContentAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('user', 'created_at')

admin.site.register(Content, ContentAdmin)