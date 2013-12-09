# -*- coding: utf-8 -*-

from django_any.models import any_model
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import Http404
from app.models import Question
from app import views


class QuestionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='I', email='i@mail.ru', password='I')
        self.question = any_model(Question, pk=1, author=self.user)

    def test_details_exist(self):
        request = self.factory.get(self.question.get_absolute_url())
        request.user = self.user
        response = views.QuestionDetail.as_view()(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 200)

    def test_details_not_exist(self):
        request = self.factory.get(reverse('question.detail', args=["0"]))
        self.assertRaises(Http404, views.QuestionDetail.as_view(), request, pk=0)

    def test_list(self):
        request = self.factory.get(reverse('question.list'))
        response = views.QuestionList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["object_list"]), 1)

    def test_create_done(self):
        request = self.factory.post(reverse('question.create'), data={'text': 'test', 'caption': 'test'})
        request.user = self.user
        response = views.QuestionCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 2)

    def test_create_fail(self):
        error = u'Обязательное поле'
        request = self.factory.post(reverse('question.create'), data={})
        request.user = self.user
        response = views.QuestionCreate.as_view()(request)
        self.assertTrue(error in response.context_data['form'].errors["text"].__unicode__())
        self.assertTrue(error in response.context_data['form'].errors["caption"].__unicode__())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)

    def test_create_fail_user(self):
        request = self.factory.post(reverse('question.create'), data={'text': 'test', 'caption': 'test'})
        request.user = AnonymousUser()
        response = views.QuestionCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

    def test_create_fail_caption(self):
        max_length = Question._meta.get_field('caption').max_length
        error = u'Убедитесь, что это значение содержит не более %d символов (сейчас %d)' % (max_length, max_length + 1)
        request = self.factory.post(reverse('question.create'), data={'text': 'test', 'caption': 't' * (max_length + 1)})
        request.user = self.user
        response = views.QuestionCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(error in response.context_data['form'].errors["caption"].__unicode__())
        self.assertEqual(Question.objects.count(), 1)

    def test_update_done(self):
        request = self.factory.post(reverse('question.update', args=(str(self.question.pk),)),
                                    data={'text': 'test', 'caption': 'test'})
        request.user = self.user
        response = views.QuestionUpdate.as_view()(request, pk=self.question.pk)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.get(pk=self.question.pk).text, 'test')
        self.assertEqual(response.status_code, 302)

    def test_update_fail_data(self):
        error = u'Обязательное поле'
        request = self.factory.post(reverse('question.update', args=(str(self.question.pk),)),
                                    data={})
        request.user = self.user
        response = views.QuestionUpdate.as_view()(request, pk=self.question.pk)
        self.assertTrue(error in response.context_data['form'].errors["text"].__unicode__())
        self.assertTrue(error in response.context_data['form'].errors["caption"].__unicode__())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.count(), 1)

    def test_update_fail_pk(self):
        request = self.factory.post(reverse('question.update', args=('0',)),
                                    data={'text': 'test', 'caption': 'test'})
        request.user = self.user
        self.assertRaises(Http404, views.QuestionUpdate.as_view(), request, pk=0)

    def test_update_fail_user(self):
        request = self.factory.post(reverse('question.update', args=(str(self.question.pk),)),
                                    data={})
        request.user = AnonymousUser()
        response = views.QuestionUpdate.as_view()(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)

    def test_update_fail_caption(self):
        max_length = Question._meta.get_field('caption').max_length
        error = u'Убедитесь, что это значение содержит не более %d символов (сейчас %d)' % (max_length, max_length + 1)
        request = self.factory.post(reverse('question.update', args=(str(self.question.pk),)),
                                    data={'text': 'test', 'caption': 't' * (max_length + 1)})
        request.user = self.user
        response = views.QuestionUpdate.as_view()(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(error in response.context_data['form'].errors["caption"].__unicode__())
        self.assertEqual(Question.objects.count(), 1)

    def test_delete_done(self):
        request = self.factory.post(reverse('question.delete', args=(str(self.question.pk),)))
        request.user = self.user
        response = views.QuestionDelete.as_view()(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_fail_pk(self):
        request = self.factory.post(reverse('question.delete', args=('0',)))
        request.user = self.user
        self.assertRaises(Http404, views.QuestionDelete.as_view(), request, pk=0)

    def test_delete_fail_user(self):
        request = self.factory.post(reverse('question.delete', args=(str(self.question.pk),)))
        request.user = AnonymousUser()
        response = views.QuestionDelete.as_view()(request, pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)