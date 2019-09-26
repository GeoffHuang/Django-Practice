from django import forms
from django.contrib import admin

from .models import Choice, Question, Company
from .models import curse_words_in_entry, CURSE_WORDS_FILEPATH


class QuestionAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        field = 'question_text'
        entry = cleaned_data.get(field)
        for curse_word in curse_words_in_entry(entry):
            msg = "Please don't use curse word: " + curse_word
            self.add_error(field, msg)


class ChoiceAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        field = 'choice_text'
        entry = cleaned_data.get(field)
        for curse_word in curse_words_in_entry(entry):
            msg = "Please don't use curse word: " + curse_word
            self.add_error(field, msg)


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'created_at', 'updated_at')


class ChoiceInline(admin.TabularInline):
    form = ChoiceAdminForm
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    form = QuestionAdminForm
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        (None,               {'fields': ['company']}),
        ('Date information', {
            'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
