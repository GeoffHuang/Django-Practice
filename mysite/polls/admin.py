from django import forms
from django.contrib import admin
# from django.contrib import messages

from .models import Choice, Question

import yaml


def contains_curse_words(entry):
    with open("polls/curse_words.yaml", 'r') as stream:
        curse_words = yaml.safe_load(stream)
    my_list = []
    for curse_word in curse_words:
        if curse_word in entry.lower():
            my_list.append(curse_word)
    return my_list

# def validate_no_curse_words(field, entry, form):
#     flag = True
#     with open("polls/curse_words.yaml", 'r') as stream:
#         curse_words = yaml.safe_load(stream)
#     for curse_word in curse_words:
#         if curse_word in entry.lower():
#             msg = "Please don't use curse word: " + curse_word
#             form.add_error(field, msg)
#             flag = False
#     return flag


class QuestionAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        field = "question_text"
        entry = cleaned_data.get(field)
        for curse_word in contains_curse_words(entry):
            msg = "Please don't use curse word: " + curse_word
            self.add_error(field, msg)


class ChoiceAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        field = "choice_text"
        entry = cleaned_data.get(field)
        for curse_word in contains_curse_words(entry):
            msg = "Please don't use curse word: " + curse_word
            self.add_error(field, msg)


class ChoiceInline(admin.TabularInline):
    form = ChoiceAdminForm
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    # template code for adding messages
    # def save_model(self, request, obj, form, change):
    #     messages.error(request, "Error Message")
    #     messages.add_message(request, messages.INFO, 'Success Message')
    #     super(QuestionAdmin, self).save_model(request, obj, form, change)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
