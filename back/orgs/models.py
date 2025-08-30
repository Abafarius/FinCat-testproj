from django.db import models
from django.core.validators import RegexValidator


bin_validator = RegexValidator(regex=r"^\d{12}$", message="BIN must be exactly 12 digits")

class License(models.Model):
    code = models.CharField(max_length=64, unique=True)
    issued_at = models.DateField(null=True, blank=True)
    def __str__(self): return self.code

class FinancialOrg(models.Model):
    name = models.CharField(max_length=255)
    bin = models.CharField(max_length=12, unique=True, validators=[bin_validator])
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    licenses = models.ManyToManyField(License, blank=True)
    def __str__(self): return f"{self.name} ({self.bin})"

