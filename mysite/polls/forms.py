from django import forms
from django.db import models

from .models import Question, Company, curse_words_in_entry
from .tasks import send_email_task, change_poll_status_task


class QuestionForm(forms.ModelForm):
    company = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ['question_text']

    def __init__(self, *args, **kwargs):
        """give {{ form.company }} an id tag for the AJAX autocomplete"""
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = forms.TextInput(
            attrs={'id': 'company'})

    def clean(self):
        cleaned_data = super().clean()
        field = 'question_text'
        entry = cleaned_data.get(field)
        for curse_word in curse_words_in_entry(entry):
            msg = "Please don't use curse word: " + curse_word
            self.add_error(field, msg)
        field = 'company'
        entry = cleaned_data.get(field)
        if not Company.objects.filter(name=entry):
            self.add_error(field, "Please enter a Fortune 100 company")

    def send_email(self):
        question_text = super().clean().get('question_text')
        q = Question.objects.get(question_text=question_text)
        body = question_text
        for choice in q.choice_set.all():
            body += "\n\u2022 " + choice.choice_text
        send_email_task.delay(body)
        change_poll_status_task.s(question_text).apply_async(countdown=5)
