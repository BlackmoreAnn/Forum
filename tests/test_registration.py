# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile


class RegistrationTestCase(TestCase):

    def test_register(self):
        response = self.client.post(reverse('registration_register'), data={'username': 'X', 'email': 'x@example.com',
                                                                            'password1': 'X', 'password2': 'X'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver%s' % reverse('registration_complete'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'Активация аккаунта – %s' % Site.objects.get_current())
        self.assertEqual(RegistrationProfile.objects.count(), 1)

    def test_activation(self):
        user = RegistrationProfile.objects.create_inactive_user(username='X', email='x@example.com',
                                                                password='x', site=Site.objects.get_current())
        response = self.client.get(reverse('registration_activate',
                                           kwargs={'activation_key': RegistrationProfile.objects.get(user=user).activation_key }))
        self.assertEqual(response.status_code, 302)