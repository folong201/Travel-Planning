from django.contrib import admin
from .models import Receptionist

@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('accommodations',)  # For a better interface when assigning accommodations
