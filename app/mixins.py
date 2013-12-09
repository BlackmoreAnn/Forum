from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from models import Question
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404


class BaseMixin(object):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BaseMixin, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseMixin, self).dispatch(request, *args, **kwargs)


class AnswerMixin(BaseMixin):

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['question_pk'])
        return super(AnswerMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('question.detail', args=(str(self.kwargs['question_pk']),))