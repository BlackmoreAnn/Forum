# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail
from forum.settings import DEFAULT_FROM_EMAIL
from django.contrib.sites.models import Site


class Question(models.Model):
    text = models.TextField()
    caption = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    date_question = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('question.detail', args=[str(self.pk)])

    class Meta:
        ordering = ("caption",)


class Answer(models.Model):
    message = models.TextField()
    author = models.ForeignKey(User)
    date_answer = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Answer, self).save(force_insert, force_update, using)
        if self.author != self.question.author:
            mail.send_mail(u'На ваш вопрос ответили!',
                           u'Посмотреть ответ можно по ссылке %s%s' % (Site.objects.get_current(), self.question.get_absolute_url()),
                           DEFAULT_FROM_EMAIL, [self.question.author.email], fail_silently=False)


# Через сигналы отправку почты можно было сделать как-то так, но я считаю это не верным решением
#
#from django.db.models.signals import post_save
#def send_mail_func(sender, instance, **kwargs):
#    if instance.author != instance.question.author:
#        mail.send_mail(u'На ваш вопрос ответили!',
#                       u'Посмотреть ответ можно по ссылке %s%s' % (Site.objects.get_current(),
#                                                                   instance.question.get_absolute_url()),
#                       DEFAULT_FROM_EMAIL, [instance.question.author.email], fail_silently=False)
#
#post_save.connect(send_mail_func, sender=Answer)