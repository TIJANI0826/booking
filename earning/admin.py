from django.contrib import admin

# Register your models here.
from .models import Package, TicketNumber , Members ,Laundry
admin.site.register(Package)
admin.site.register(TicketNumber)
admin.site.register(Members)
admin.site.register(Laundry)