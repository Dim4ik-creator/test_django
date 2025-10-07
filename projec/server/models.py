from django.db import models

class Leader(models.Model):
    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50, blank=False, unique=True)
    company = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128, blank=False)
    

    def __str__(self):
        return self.name
    

class Candidante(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    email = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=128, blank=False)


    def __str__(self):
        return self.name