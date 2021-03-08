from django.contrib import admin

# Register your models here.
# TO make the Messages show up in the admin panel.
from chats.models import Message
admin.site.register(Message)