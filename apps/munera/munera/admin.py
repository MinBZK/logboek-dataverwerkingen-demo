from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from munera.models import User


admin.site.site_header = "Mijn Gemeente"
admin.site.site_title = "Mijn Gemeente admin"
admin.site.index_title = "Administration"


class UserAdmin(BaseUserAdmin):
    fieldsets = (("Munera", {"fields": ["bsn"]}),) + BaseUserAdmin.fieldsets


admin.site.register(User, UserAdmin)
