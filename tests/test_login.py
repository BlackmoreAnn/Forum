# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_any.models import any_model
from app.models import Question, Answer


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='I', email='i@mail.ru', password='I')
        self.question = any_model(Question, pk=1, author=self.user)
        self.answer = any_model(Answer, pk=1, author=self.user, question=self.question)

    def test_login_redirect(self):
        for url in [reverse('question.create'), reverse('question.update', args=(str(self.question.pk),)),
                    reverse('question.delete', args=(str(self.question.pk),)),
                    reverse('answer.create', args=(str(self.question.pk),)),
                    reverse('answer.update', args=(str(self.question.pk), str(self.answer.pk))),
                    reverse('answer.delete', args=(str(self.question.pk), str(self.answer.pk)))]:
            response = self.client.get(url)
            self.assertRedirects(response, '/accounts/login/?next=' + url)

    def test_not_login(self):
        for url in [reverse('question.list'), reverse('question.detail', args=(str(self.question.pk),))]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_login_done(self):
        response = self.client.post(reverse('auth_login'), data={'username': 'I', 'password': 'I'})
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse('auth_login'), data={'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Неверное имя пользователя или пароль.')