from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, tg_login, tg_name, password=None):
        if len(tg_name) == 0 or len(tg_login) == 0:
            raise ValueError('User must have telegram login and name')

        user = self.model(tg_login=tg_login, tg_name=tg_name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, tg_login, tg_name, password):
        user = self.create_user(tg_login, tg_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.type = User.Type.ADMIN,
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        USER      = 'usr'
        EXPERT    = 'exp'
        ADMIN     = 'adm'
        MODERATOR = 'mod'
        BOT       = 'bot'

    tg_login = models.CharField(max_length=255, unique=True)
    tg_name = models.CharField(max_length=255)
    resource_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'tg_login'
    REQUIRED_FIELDS = ['tg_name']

    def __str__(self):
        return self.tg_login

    
class Question(models.Model):
    class Status(models.TextChoices):
        ACTIVE   = 'active'
        SOLVED   = 'solved'
        REJECTED = 'rejected'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )
    resource_id = models.PositiveIntegerField(unique=True, blank=True, null=True)

    
class Message(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)


class ChatMember(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    