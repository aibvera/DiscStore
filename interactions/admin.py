from django.contrib import admin
from .models import Artist, Album, Order, Order_Detail

# Register your models here.

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Order)
admin.site.register(Order_Detail)
