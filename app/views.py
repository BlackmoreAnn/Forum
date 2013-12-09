from django.views import generic
from django.views.generic.detail import SingleObjectMixin
from models import Question, Answer
from mixins import BaseMixin, AnswerMixin
from django.core.urlresolvers import reverse_lazy


class QuestionList(generic.ListView):
    model = Question
    paginate_by = 5


class QuestionDetail(SingleObjectMixin, generic.ListView):
    template_name = "app/question_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Question.objects.all())
        return super(QuestionDetail, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.answer_set.all()


class QuestionCreate(BaseMixin, generic.CreateView):
    model = Question
    fields = ('caption', 'text')


class QuestionUpdate(BaseMixin, generic.UpdateView):
    model = Question
    fields = ('caption', 'text')


class QuestionDelete(BaseMixin, generic.DeleteView):
    model = Question
    success_url = reverse_lazy('question.list')


class AnswerCreate(AnswerMixin, generic.CreateView):
    model = Answer
    fields = ('message',)


class AnswerUpdate(AnswerMixin, generic.UpdateView):
    model = Answer
    fields = ('message',)


class AnswerDelete(AnswerMixin, generic.DeleteView):
    model = Answer