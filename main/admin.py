from django.contrib import admin
from main.models import NormalUser, Teacher


@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class NormalUserTeacher(admin.ModelAdmin):
    pass
