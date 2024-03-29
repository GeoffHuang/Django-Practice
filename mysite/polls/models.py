import datetime

from django import forms
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, inlineformset_factory, TextInput
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

import yaml

CURSE_WORDS_FILEPATH = "polls/curse_words.yaml"


def curse_words_in_entry(entry):
    """
    returns a list of curse words in entry
    returns empty list if entry has no curse words
    (curse words are listed in curse_words.yaml)
    """
    with open(CURSE_WORDS_FILEPATH, 'r') as stream:
        curse_words = yaml.safe_load(stream)
    my_list = []
    for curse_word in curse_words:
        if curse_word in entry.lower().split():
            my_list.append(curse_word)
    return my_list


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, null=True)
    classification = models.CharField(max_length=3, default="B2A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"


class Question(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def save(self, *args, **kwargs):
        if curse_words_in_entry(str(self)):
            print("Please do not submit question text containing curse words.")
        else:
            super(Question, self).save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def clean(self):
        if curse_words_in_entry(str(self)):
            raise ValidationError("Please don't use curse words!!")

    def save(self, *args, **kwargs):
        if curse_words_in_entry(str(self)):
            print("Please do not submit choice text containing curse words.")
        else:
            super(Choice, self).save(*args, **kwargs)


class QuestionForm(ModelForm):
    company = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ['question_text']

    # give {{ form.company }} an id tag for the AJAX autocomplete
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['company'].widget = TextInput(
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
