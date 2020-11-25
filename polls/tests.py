import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
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
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


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
        Questions with a pub_date in the past AND 
        at least two choices are displayed on the index page.
        """
        q = create_question(question_text="Past question with two choices.", days=-30)
        q.choice_set.create(choice_text='Not much')
        q.choice_set.create(choice_text='The sky')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question with two choices.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future AND 
        at least two choices aren't displayed on the index page.
        """
        q = create_question(question_text="Future question with two choices.", days=30)
        q.choice_set.create(choice_text='Not much')
        q.choice_set.create(choice_text='The sky')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        q1 = create_question(question_text="Past question with two choices.", days=-30)
        q1.choice_set.create(choice_text='Not much')
        q1.choice_set.create(choice_text='The sky')
        q2 = create_question(question_text="Future question with two choices.", days=30)
        q2.choice_set.create(choice_text='Not much')
        q2.choice_set.create(choice_text='The sky')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question with two choices.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions
        WITH at least two choices.
        """
        q1 = create_question(question_text="Past question 1.", days=-30)
        q1.choice_set.create(choice_text='Not much')
        q1.choice_set.create(choice_text='The sky')
        q2 = create_question(question_text="Past question 2.", days=-5)
        q2.choice_set.create(choice_text='Not much')
        q2.choice_set.create(choice_text='The sky')
        q2.choice_set.create(choice_text='To infinity')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_two_past_questions_and_only_one_with_at_least_two_choices(self):
        """
        Even if both past questions exist, only the question
        with at least two choices is displayed.
        """
        q1 = create_question(question_text="Past question with two choices.", days=-30)
        q1.choice_set.create(choice_text='Not much')
        q1.choice_set.create(choice_text='The sky')
        q2 = create_question(question_text="Past question with one choice.", days=-30)
        q2.choice_set.create(choice_text='Not much')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question with two choices.>']
    )

    def test_past_questions_with_less_than_two_choices(self):
        """
        Past questions with only with only one choice is not displayed.
        """
        q1 = create_question(question_text="Past question with only one choice.", days=-30)
        q1.choice_set.create(choice_text='Not much')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], []
    )

    def test_logged_in_admin_users_can_see_unpublished_questions(self):
        """
        Logged-in admin users are allowed to see all questions
        even future unpublished ones.
        """
        password = 'mypassword'
        admin_user = get_user_model().objects.create_superuser('myuser', 'myemail@test.com', password)
        self.client.login(username=admin_user.username, password=password)
        q = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Future question.")


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The results view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
