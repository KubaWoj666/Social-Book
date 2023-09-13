from django.contrib import admin

from .models import ChatModel

class adminChat(admin.ModelAdmin):
    list_display = ["message", "sender", "thread_name"]

admin.site.register(ChatModel, adminChat)
