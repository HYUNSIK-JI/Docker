from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.views import status

from django.shortcuts import resolve_url
from django.urls import reverse
from .models import *


class YourTestClass(TestCase):
    def setUp(self):
        
        pass

    def tearDown(self):
        
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)