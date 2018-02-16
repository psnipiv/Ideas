from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import NewIdeaForm
from ..models import Discipline,Idea,Post
from ..views import new_idea


# Create your tests here.

class NewIdeaTests(TestCase):
    def setUp(self):
        Discipline.objects.create(name='Test', description='Test Description.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  # <- included this line here
        self.client.login(username='john', password='123')

    def test_new_idea_view_success_status_code(self):
        url = reverse('new_idea', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_idea_view_not_found_status_code(self):
        url = reverse('new_idea', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_idea_url_resolves_new_idea_view(self):
        view = resolve('/disciplines/1/new/')
        self.assertEquals(view.func, new_idea)

    def test_new_idea_view_contains_link_back_to_discipline_ideas_view(self):
        new_idea_url = reverse('new_idea', kwargs={'pk': 1})
        discipline_ideas_url = reverse('discipline_ideas', kwargs={'pk': 1})
        response = self.client.get(new_idea_url)
        self.assertContains(response, 'href="{0}"'.format(discipline_ideas_url))
    
    def test_csrf(self):
        url = reverse('new_idea', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_idea_valid_post_data(self):
        url = reverse('new_idea', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Test message'
        }
        response = self.client.post(url, data)
        self.assertTrue(Idea.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_idea_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_idea', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_idea_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_idea', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Idea.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):  # <- new test
        url = reverse('new_idea', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewIdeaForm)

    def test_new_idea_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_idea', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Discipline.objects.create(name='Test', description='Test Description')
        self.url = reverse('new_idea', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))