from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Discipline, Post, Idea
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        discipline = Discipline.objects.create(name='Test', description='Test Description')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        idea = Idea.objects.create(subject='Test Idea', discipline=discipline, starter=user)
        Post.objects.create(message='This is a test post', idea=idea, created_by=user)
        url = reverse('idea_posts', kwargs={'pk': discipline.pk, 'idea_pk': idea.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/disciplines/1/ideas/1/')
        self.assertEquals(view.func.view_class, PostListView)