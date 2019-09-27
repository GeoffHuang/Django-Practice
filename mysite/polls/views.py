from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms import inlineformset_factory
from django.contrib import messages

from .models import Choice, Question, Company
from .forms import QuestionForm

import json
import csv

CSV_FILEPATH = "polls/static/polls/vote_data.csv"


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last ten published questions (not including those set to
        be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    with open(CSV_FILEPATH, 'wt') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',)
        csv_writer.writerow(['name', 'value'])
        for choice in question.choice_set.all():
            csv_writer.writerow([choice.choice_text, choice.votes])
    return render(request, 'polls/results.html', {'question': question})


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
    ChoiceFormSet = inlineformset_factory(
        Question, Choice, fields=('choice_text',), extra=4)
    if request.method == 'POST':
        company_name = request.POST.get('company')
        if not Company.objects.filter(name=company_name):
            company = get_object_or_404(Company, pk=1)
        else:
            company = Company.objects.get(name=company_name)
        q = Question(company=company)
        q.status = "processing"
        form = QuestionForm(request.POST, instance=q)
        formset = ChoiceFormSet(request.POST, instance=q)
        if form.is_valid() and formset.is_valid():
            new_question = form.save()
            for choice in formset:
                new_choice = choice.save(commit=False)
                new_choice.question = new_question
                new_choice.save()
            form.send_email()
            return HttpResponseRedirect(reverse('polls:index'))
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    return render(request, 'polls/submit.html', {
        'form': form, 'formset': formset})


def company_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        companies = Company.objects.filter(name__startswith=q)[:20]
        results = []
        for company in companies:
            company_json = {}
            company_json['value'] = company.name
            results.append(company_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
