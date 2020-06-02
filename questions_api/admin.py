from django.contrib import admin

from questions_api import models


admin.site.register(models.User)
admin.site.register(models.Question)
admin.site.register(models.Message)
admin.site.register(models.ChatMember)