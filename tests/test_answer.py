# -*- coding: utf-8 -*-

from django_any.models import any_model
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.http import Http404
from app.models import Question, Answer
from app import views
from django.core import mail


class QuestionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.question_user = User.objects.create_user(
            username='I', email='i@mail.ru', password='I')

        self.answer_user = User.objects.create_user(
            username='A', email='a@mail.ru', password='A')
        self.question = any_model(Question, pk=1, author=self.question_user)
        self.answer = any_model(Answer, pk=1, author=self.question_user, question=self.question)

    def test_create_done(self):
        request = self.factory.post(reverse('answer.create', args=(str(self.question.pk),)),
                                    data={'message': "this is answer"})
        request.user = self.answer_user
        response = views.AnswerCreate.as_view()(request, question_pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'На ваш вопрос ответили!')

    def test_create_done_owner(self):
        request = self.factory.post(reverse('answer.create', args=(str(self.question.pk),)),
                                    data={'message': "this is answer"})
        request.user = self.question_user
        response = views.AnswerCreate.as_view()(request, question_pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 0)

    def test_create_fail_message(self):
        error = u'Обязательное поле'
        request = self.factory.post(reverse('answer.create', args=(str(self.question.pk),)), data={})
        request.user = self.question_user
        response = views.AnswerCreate.as_view()(request, question_pk=self.question.pk)
        self.assertTrue(error in response.context_data['form'].errors["message"].__unicode__())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Answer.objects.count(), 1)

    def test_create_fail_user(self):
        request = self.factory.post(reverse('answer.create', args=(str(self.question.pk),)),
                                    data={'message': "this is answer"})
        request.user = AnonymousUser()
        response = views.AnswerCreate.as_view()(request, question_pk=self.question.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)

    def test_create_fail_question(self):
        request = self.factory.post(reverse('answer.create', args=('0',)), data={"message": "New message"})
        request.user = self.question_user
        self.assertRaises(Http404, views.AnswerCreate.as_view(), request, question_pk=0)

    def test_update_done(self):
        request = self.factory.post(reverse('answer.update', args=(str(self.question.pk), str(self.answer.pk))),
                                    data={'message': "this is new answer"})
        request.user = self.answer_user
        response = views.AnswerUpdate.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'На ваш вопрос ответили!')

    def test_update_done_owner(self):
        request = self.factory.post(reverse('answer.update', args=(str(self.question.pk), str(self.answer.pk))),
                                    data={'message': "this is new answer"})
        request.user = self.question_user
        response = views.AnswerUpdate.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_update_fail_message(self):
        error = u'Обязательное поле'
        request = self.factory.post(reverse('answer.update', args=(str(self.question.pk), str(self.answer.pk))),
                                    data={})
        request.user = self.answer_user
        response = views.AnswerUpdate.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertTrue(error in response.context_data['form'].errors["message"].__unicode__())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Answer.objects.count(), 1)

    def test_update_fail_user(self):
        request = self.factory.post(reverse('answer.update', args=(str(self.question.pk), str(self.answer.pk))),
                                    data={'message': "this is answer"})
        request.user = AnonymousUser()
        response = views.AnswerUpdate.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)

    def test_update_fail_question(self):
        request = self.factory.post(reverse('answer.update', args=('0', self.answer.pk)),
                                    data={"message": "New message"})
        request.user = self.question_user
        self.assertRaises(Http404, views.AnswerUpdate.as_view(), request, question_pk=0, pk=self.answer.pk)

    def test_delete_done(self):
        request = self.factory.post(reverse('answer.delete', args=(str(self.question.pk), str(self.answer.pk))))
        request.user = self.question_user
        response = views.AnswerDelete.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 0)

    def test_delete_fail_answer_pk(self):
        request = self.factory.post(reverse('answer.delete', args=(str(self.question.pk), '0')))
        request.user = self.question_user
        self.assertRaises(Http404, views.AnswerDelete.as_view(), request, question_pk=self.question.pk, pk=0)

    def test_delete_fail_user(self):
        request = self.factory.post(reverse('answer.delete', args=(str(self.question.pk), str(self.answer.pk))))
        request.user = AnonymousUser()
        response = views.AnswerDelete.as_view()(request, question_pk=self.question.pk, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 1)

    def test_delete_fail_question(self):
        request = self.factory.post(reverse('answer.delete', args=('0', self.answer.pk)))
        request.user = self.question_user
        response = views.AnswerDelete.as_view()(request, question_pk=0, pk=self.answer.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), 0)
