from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from ..models import Discipline
from ..views import DisciplineListView


class HomeTests(TestCase):
    def setUp(self):
        self.discipline = Discipline.objects.create(name='Test', description='Test Description.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  # <- included this line here
        self.client.login(username='john', password='123')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, DisciplineListView)

    def test_home_view_contains_link_to_ideas_page(self):
        discipline_ideas_url = reverse('discipline_ideas', kwargs={'pk': self.discipline.pk})
        self.assertContains(self.response, 'href="{0}"'.format(discipline_ideas_url))