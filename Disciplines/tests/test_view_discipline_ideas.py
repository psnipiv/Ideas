from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Discipline
from ..views import IdeaListView

class DisciplineIdeasTests(TestCase):
    def setUp(self):
        Discipline.objects.create(name='Test', description='Test Section.')
        User.objects.create_user(username='john', email='john@doe.com', password='123')  # <- included this line here
        self.client.login(username='john', password='123')

    def test_discipline_ideas_view_success_status_code(self):
        url = reverse('discipline_ideas', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_discipline_ideas_view_not_found_status_code(self):
        url = reverse('discipline_ideas', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/disciplines/1/')
        self.assertEquals(view.func.view_class, IdeaListView)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        discipline_ideas_url = reverse('discipline_ideas', kwargs={'pk': 1})
        response = self.client.get(discipline_ideas_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
        discipline_ideas_url = reverse('discipline_ideas', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_idea_url = reverse('new_idea', kwargs={'pk': 1})

        response = self.client.get(discipline_ideas_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_idea_url))

    def test_discipline_ideas_url_resolves_discipline_ideas_view(self):
        view = resolve('/disciplines/1/')
        self.assertEquals(view.func.view_class, IdeaListView)