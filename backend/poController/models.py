from datetime import timedelta
from django.db import models

class POGaurd(models.Model):
    poNumber = models.PositiveIntegerField(unique=True)
    sent_to_vendor = models.BooleanField(default=True)
    isConfirmed = models.BooleanField(default=False)
    hasNotified = models.BooleanField(default=False)
    hasError = models.BooleanField(default=False)
    sent_datetime = models.DateTimeField(auto_now_add=True)
    vendor = models.CharField(max_length=100, blank=True, null=True)
    errorMsg = models.CharField(max_length=500, blank=True, null=True)
    waiting_time_for_confirmation = models.PositiveSmallIntegerField(default=24)
    
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.poNumber)
    
    @property
    def expected_confirmation_time(self):
        return self.sent_datetime + timedelta(hours=self.waiting_time_for_confirmation)
