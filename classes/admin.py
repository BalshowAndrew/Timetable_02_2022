from django.contrib import admin

from .models import *


class Start_classAdmin(admin.ModelAdmin):
    list_display = ('id', 'time')


class ClassesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'category',
        'course',
        'faculty',
        'language',
        'group',
        'start_day',
        'start',
        'end_day',
        'teacher',
    )
    list_filter = (
        'category',
        'course',
        'faculty',
        'language',
        'teacher'
    )


admin.site.register(Start_class, Start_classAdmin)
admin.site.register(Classes, ClassesAdmin)
