from django.contrib import admin
from .models import Profile, Destination, Accommodation, Hotel, Booking, Agency

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'address', 'travel_preferences', 'profile_picture')
    search_fields = ('full_name', 'user__username', 'phone_number')
    list_filter = ('user',)
admin.site.register(Profile, ProfileAdmin)

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'popular_attractions', 'image')
    search_fields = ('name', 'city', 'popular_attractions')
admin.site.register(Destination, DestinationAdmin)

class AccommodationAdmin(admin.ModelAdmin):
    search_fields = ('type_of_accommodation', 'name', 'town')
    list_display = ("name", "town", 'location', "price_per_night", "type_of_accommodation", "phone_number")
admin.site.register(Accommodation, AccommodationAdmin)

admin.site.register(Hotel)

class BookingAdmin(admin.ModelAdmin):
    list_filter = ("user", "accommodation", "check_in_date", "check_out_date", "total_price")
admin.site.register(Booking, BookingAdmin)

class AgencyAdmin(admin.ModelAdmin):
    list_filter = ('name', 'location', 'simple_price', 'classic_price', 'vip_price')
admin.site.register(Agency, AgencyAdmin)
