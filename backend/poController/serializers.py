from rest_framework import serializers
from .models import POGaurd

class POGaurdSerializer(serializers.ModelSerializer):
    expected_confirmation_time = serializers.SerializerMethodField()
    
    class Meta:
        model = POGaurd
        fields = [
            'id',
            'poNumber',
            'sent_to_vendor',
            'isConfirmed',
            'hasNotified',
            'sent_datetime',
            'hasError',
            'errorMsg',
            'vendor',
            'waiting_time_for_confirmation',
            'modified_at',
            'expected_confirmation_time'
        ]
        
    def get_expected_confirmation_time(self, obj):
        return obj.expected_confirmation_time
    
    def to_internal_value(self, data):
        if 'vendor' in data:
            data['vendor'] = data['vendor'].capitalize()
        return super().to_internal_value(data)