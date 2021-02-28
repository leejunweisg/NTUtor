from django.contrib import admin
from .models import  Module, Listing, TuitionSession

# Register your models here.
admin.site.register(Module)
admin.site.register(Listing)
admin.site.register(TuitionSession)