from django.contrib import admin
from .models import POGaurd

@admin.register(POGaurd)
class POGaurdAdmin(admin.ModelAdmin):
    list_display = ('id', 'poNumber', 'sent_to_vendor', 'isConfirmed')