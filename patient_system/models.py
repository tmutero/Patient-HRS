# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Patient(models.Model):
    firstname = models.CharField(max_length=40, blank=False)
    lastname = models.CharField(max_length=40, blank=False)
    mobile_number = models.CharField(max_length=10, blank=True)
    gender = models.TextField(max_length=10, blank=False)
    address = models.TextField(max_length=255, blank=False)
    date_of_birth = models.DateField('%m/%d/%Y')
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S')

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.CharField(max_length=255,)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True)


class Prescription(models.Model):
    text = models.CharField(max_length=255, blank=True)
    medication = models.EmailField(max_length=254)
    dosage = models.CharField(max_length=100, blank=True)
    frequency = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    expiration_at = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


