from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import inlineformset_factory

from .models import Choice, Question, Company, QuestionForm

import json


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last twenty published questions (not including those set to
        be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:20]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))


def submission(request):
    QuestionFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',))
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = QuestionFormSet(request.POST, request.FILES, instance=Question())
        if form.is_valid() and formset.is_valid():
            new_question = form.save()
            for choice in formset:
                new_choice = choice.save(commit=False)
                new_choice.question = new_question
                new_choice.save()
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = QuestionForm()
        formset = QuestionFormSet(instance=Question())
    return render(request, 'polls/submit.html', {'form': form, 'formset': formset})


def autocompleteModel(request):
    print("TEST")
    console.log("test")
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Company.objects.filter(name__startswith=q)
        results = []
        print(q)
        for r in search_qs:
            r_json = {}
            r_json['id'] = r.name
            r_json['label'] = r.name
            r_json['value'] = r.name
            results.append(r_json)
            #results.append(r.FIELD)
        data = json.dumps(results)
        print(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_company(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        companies = Company.objects.filter(name__startswith=q)[:20]
        results = []
        for company in companies:
            company_json = {}
            # company_json['id'] = company.name
            # company_json['label'] = company.name
            company_json['value'] = company.name
            results.append(company_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
