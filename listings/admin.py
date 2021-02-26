from django.contrib import admin
from .models import School, Module, Listing, TuitionSession

# Register your models here.
admin.site.register(School)
admin.site.register(Module)
admin.site.register(Listing)
admin.site.register(TuitionSession)