from django.contrib import admin
from .models import Profiles


class ProfilesAdmin(admin.ModelAdmin):
    search_fields = ("address", "bio", "certificate", "country", "email2", "name", "phone", "phone2", "publications_count", "specialist", "specific_specialist", "user_type", "work_address")
admin.site.register(Profiles, ProfilesAdmin)
