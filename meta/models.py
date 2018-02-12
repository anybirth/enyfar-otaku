from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50)
    is_supported = models.BooleanField()

    class Meta:
        verbose_name = "country"
        verbose_name_plural = 'countries'

    def __str__(self):
        return '%s' % self.name

class District(models.Model):
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=50, blank=True)
    is_supported = models.BooleanField()

    class Meta:
        verbose_name = "district"
        verbose_name_plural = 'districts'

    def __str__(self):
        return '%s' % self.name
