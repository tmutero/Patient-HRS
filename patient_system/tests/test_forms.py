"""
Unit tests for django-registration.

These tests assume that you've completed all the prerequisites for
getting django-registration running in the default setup, to wit:

1. You have ``registration`` in your ``INSTALLED_APPS`` setting.

2. You have created all of the templates mentioned in this
   application's documentation.

3. You have added the setting ``ACCOUNT_ACTIVATION_DAYS`` to your
   settings file.

4. You have URL patterns pointing to the registration and activation
   views, with the names ``registration_register`` and
   ``registration_activate``, respectively, and a URL pattern named
   'registration_complete'.

"""

from django.conf import settings

from django.contrib.auth.models import User as user_model

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db.models import get_model

from patient_system import forms


class RegistrationTestCase(TestCase):
    """
    Base class for the test cases; this sets up two users -- one
    expired, one not -- which are used to exercise various parts of
    the application.
    """
    def setUp(self):
        self.sample_user = user_model.objects.create(username='alice',
                                                                            password='secret',
                                                                            email='alice@example.com',
                                                                             is_active=True)
        self.sample_user.save()
        


class RegistrationModelTests(RegistrationTestCase):
    """
    Tests for the model-oriented functionality of django-registration,
    including ``RegistrationProfile`` and its custom manager.
    
    """
    def test_new_user_is_inactive(self):
        """
        Test that a newly-created user is inactive.
        
        """
        self.failIf(self.sample_user.is_active)

    def test_registration_profile_created(self):
        """
        Test that a ``Registration`` is created for a new user.
        
        """
        self.assertEqual(user_model.objects.count(), 1)


class RegistrationFormTests(RegistrationTestCase):
    """
    Tests for the forms and custom validation logic included in
    django-registration.
    
    """
    def test_registration_form(self):
        """
        Test that ``RegistrationForm`` enforces username constraints
        and matching passwords.
        
        """
        invalid_data_dicts = [
            # Non-alphanumeric username.
            {
            'data':
            { 'username': 'foo/bar',
              'email': 'foo@example.com',
              'password1': 'foo',
              'password2': 'foo' },
            'error':
            ('username', [u"Enter a valid value."])
            },
            # Already-existing username.
            {
            'data':
            { 'username': 'alice',
              'email': 'alice@example.com',
              'password1': 'secret',
              'password2': 'secret' },
            'error':
            ('username', [u"This username is already taken. Please choose another."])
            },
            # Mismatched passwords.
            {
            'data':
            { 'username': 'foo',
              'email': 'foo@example.com',
              'password1': 'foo',
              'password2': 'bar' },
            'error':
            ('__all__', [u"You must type the same password each time"])
            },
            ]

        for invalid_dict in invalid_data_dicts:
            form = forms.RegistrationForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])

        form = forms.RegistrationForm(data={ 'username': 'foo',
                                             'email': 'foo@example.com',
                                             'password1': 'foo',
                                             'password2': 'foo' })
        self.failUnless(form.is_valid())

 



    
  