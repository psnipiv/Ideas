from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve,reverse
from ..forms import PostForm
from ..models import Discipline, Post, Idea
from ..views import reply_idea


class ReplyIdeaTestCase(TestCase):
    '''
    Base test case to be used in all `reply_idea` view tests
    '''
    def setUp(self):
        self.discipline = Discipline.objects.create(name='Test', description='Test Description')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.idea = Idea.objects.create(subject='This is a test idea', discipline=self.discipline, starter=user)
        Post.objects.create(message='This is a test post', idea=self.idea, created_by=user)
        self.url = reverse('reply_idea', kwargs={'pk': self.discipline.pk, 'idea_pk': self.idea.pk})

class LoginRequiredReplyIdeaTests(ReplyIdeaTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class ReplyIdeaTests(ReplyIdeaTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/disciplines/1/ideas/1/reply/')
        self.assertEquals(view.func, reply_idea)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)

class SuccessfulReplyIdeaTests(ReplyIdeaTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        url = reverse('idea_posts', kwargs={'pk': self.discipline.pk, 'idea_pk': self.idea.pk})
        idea_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, idea_posts_url)

    def test_reply_created(self):
        '''
        The total post count should be 2
        The one created in the `ReplyIdeaTestCase` setUp
        and another created by the post data in this class
        '''
        self.assertEquals(Post.objects.count(), 2)

class InvalidReplyIDeaTests(ReplyIdeaTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_idea` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)