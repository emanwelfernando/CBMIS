from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin\

from . models import *
from .forms import *


class TouristSpotAdmin(OSMGeoAdmin):
    form = TouristSpotAdminForm
    default_zoom = 15

class HouseholdAdmin(OSMGeoAdmin):
    form = HouseholdAdminForm
    default_zoom = 15


admin.site.register(CustomUser)
admin.site.register(Resident)
admin.site.register(Health)
admin.site.register(Economic)
admin.site.register(Education)
admin.site.register(Household, HouseholdAdmin)
admin.site.register(Municipal)
admin.site.register(Barangay)
admin.site.register(TouristSpot, TouristSpotAdmin)