from django.contrib import admin
from main.models import NormalUser


@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    pass
