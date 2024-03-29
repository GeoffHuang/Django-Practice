import datetime

from django import forms
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice
from .models import curse_words_in_entry, CURSE_WORDS_FILEPATH


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions
        whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class CurseWordTests(TestCase):
    def test_no_curse_words(self):
        """
        curse_words_in_entry(entry) returns empty list if a user
        entry contains no curse words
        """
        entry = "a perfectly clean sentence with no curse words"
        expected = []
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_entry_is_curse_word(self):
        """
        curse_words_in_entry(entry) returns the proper curse word
        when a user submission is a curse word
        """
        entry = "heck"
        expected = ["heck"]
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_entry_contains_curse_word(self):
        """
        curse_words_in_entry(entry) returns the proper curse word
        when a user submission contains a curse word
        """
        entry = "testhella"
        expected = ["hella"]
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_curse_word_weird_capitalization(self):
        """
        curse_words_in_entry(entry) returns the proper curse word
        when a user submission contains a curse word irregardless of
        capitalization
        """
        entry = "test CRimInY test"
        expected = ["criminy"]
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_multiple_curse_words(self):
        """
        curse_words_in_entry(entry) returns the proper curse words
        when a user submission contains multiple curse words
        """
        entry = "heck geez criminy"
        expected = ["heck", "criminy", "geez"]
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_multiple_of_same_curse_word(self):
        """
        curse_words_in_entry(entry) returns a single curse word even
        if that curse word appears more than once
        """
        entry = "heck heckheck"
        expected = ['heck']
        self.assertEqual(curse_words_in_entry(entry), expected)

    def test_curse_word_entry_with_punctuation(self):
        """
        curse_words_in_entry(entry) returns the proper curse words even
        if the curse words are separated by punctuation
        """
        entry = "heck.hella?criminy"
        expected = ['heck', 'hella', 'criminy']
        self.assertEqual(curse_words_in_entry(entry), expected)
