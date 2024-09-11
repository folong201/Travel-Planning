from django.contrib import admin
from .models import Profile, Destination

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'address', 'travel_preferences', 'profile_picture')
    search_fields = ('full_name', 'user__username', 'phone_number')
    list_filter = ('user',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Destination)
