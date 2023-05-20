from django.contrib.auth.models import AbstractUser
from main.models import NormalUser, Teacher


def normal_user_test(user: AbstractUser) -> bool:
    return bool(NormalUser.objects.filter(user=user))


def teacher_user_test(user: AbstractUser) -> bool:
    normal_user = NormalUser.objects.filter(user=user).first()
    if normal_user:
        return bool(Teacher.objects.filter(normal_user=normal_user, is_active=True))
    else:
        return False
