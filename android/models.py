from django.db import models

# Create your models here.
class VerifyMobile(models.Model):
    token = models.CharField(max_length=200, primary_key=True)
    number = models.CharField(max_length=13, blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.otp} {self.number} {self.token}"

    
