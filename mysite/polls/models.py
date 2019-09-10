import datetime

from django.db import models
from django.utils import timezone

import yaml

curse_words_filepath = "polls/curse_words.yaml"


def contains_curse_words(entry):
    """
    returns a list of curse words in entry
    returns empty list if entry has no curse words
    (curse words are listed in curse_words.yaml)
    """
    with open(curse_words_filepath, 'r') as stream:
        curse_words = yaml.safe_load(stream)
    my_list = []
    for curse_word in curse_words:
        if curse_word in entry.lower():
            my_list.append(curse_word)
    return my_list


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def save(self, *args, **kwargs):
        if contains_curse_words(str(self)):
            print("Please do not submit question text containing curse words.")
        else:
            super(Question, self).save(*args, **kwargs)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def save(self, *args, **kwargs):
        if contains_curse_words(str(self)):
            print("Please do not submit choice text containing curse words.")
        else:
            super(Question, self).save(*args, **kwargs)
