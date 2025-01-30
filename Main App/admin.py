from django.contrib import admin
from .models import Location,Services,Person_info,Profile,Booking
from django.contrib.auth.models import Group
# Register your models here.
admin.site.register(Location)
admin.site.register(Services)
# admin.site.register(Person_info)

class PersonInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_name', 'service_name')

admin.site.register(Person_info, PersonInfoAdmin)

admin.site.register(Profile)
admin.site.register(Booking)

admin.site.unregister(Group)
admin.site.site_header = "ON-DEMANDING SERVICES  Administration"



# admin.site.register(Rough)
