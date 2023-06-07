from django.db import models
from django.urls import reverse
from datetime import date, timedelta, datetime
from django.utils.timezone import now
from django.utils import timezone
from time import localtime

from django.contrib.auth.models import User


# Create your models here.

class Pharmacy(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=200, help_text='Please include City and State')
    phoneNumber = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pharmacies_detail', kwargs={'pk': self.id})

class Medication(models.Model):
    name = models.CharField(max_length=150)
    dose = models.CharField(max_length=150)
    frequency = models.PositiveBigIntegerField(help_text='Enter the frequency in hours')
    warnings = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacies = models.ManyToManyField(Pharmacy)

    def __str__(self):
        return f'{self.name}({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'medication_id': self.id})
    
    def dose_taken(self):
        # return self.medicationintake_set.filter(timestamp__lte=now()).count() 
        last_dose = self.medicationintake_set.latest('timestamp')
        next_dose_timestamp = last_dose.timestamp + timedelta(hours=self.frequency)
        current_time = timezone.localtime(timezone.now())
        time_until_next_dose = next_dose_timestamp - current_time
        if time_until_next_dose.total_seconds() > 1850:
            return True, round(time_until_next_dose.total_seconds()/3600, 1)
        else: 
            return False
    
class MedicationIntake(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)


    def __str__(self):
        return f"A dose of {self.medication} was taken at {self.timestamp}"
    



    