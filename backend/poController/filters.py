import django_filters
from .models import POGaurd

class POGaurdFilter(django_filters.FilterSet):
    class Meta:
        model = POGaurd
        fields = ['poNumber' ,'isConfirmed', 'hasNotified', 'vendor', 'waiting_time_for_confirmation']