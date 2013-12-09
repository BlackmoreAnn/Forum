# -*- coding: utf-8 -*-

from django_any.models import any_model
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from app.models import Question


class QuestionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='I', email='i@mail.ru', password='I')

    def test_unicode(self):
        question = any_model(Question, pk=1, author=self.user, caption="test")
        self.assertEquals(question.__unicode__(), "test")