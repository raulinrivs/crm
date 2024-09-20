from django.contrib import admin
from django.contrib.auth.models import Group
from filial.models import Filial

# Register your models here.
admin.site.register(Filial)
admin.site.unregister(Group)
