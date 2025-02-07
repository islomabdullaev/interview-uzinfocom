from django.contrib import admin

from booking.models import Playground, PlaygroundBooking, PlaygroundImageItem

# Register your models here.
admin.site.register(Playground)
admin.site.register(PlaygroundImageItem)
admin.site.register(PlaygroundBooking)
