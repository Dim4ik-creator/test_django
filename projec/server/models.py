from django.db import models

class Leader(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    email = models.CharField(max_length=50, blank=False)
    name_company = models.CharField(max_length=50, blank=False)
    city_company = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128, blank=False)
    

    def __str__(self):
        return self.name
    

class Candidante(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    email = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128, blank=False)


    def __str__(self):
        return self.name