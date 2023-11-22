
import datetime
import json

from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock
from ..models import Patient, Document, Prescription



class PatientTest(TestCase):

    def setUp(self):
        Patient.objects.create(
            firstname="tafadzwa",
            lastname="Mutero",
            mobile_number="0640605016",
            gender="Male",
            address="105 Table View",
            date_of_birth= "01/01/2000",
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(), 
        )

    def tearDown(self):
        Patient.objects.all().delete()


  