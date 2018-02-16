from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Discipline, Post, Idea
from ..views import reply_idea

class ReplyIdeaTestCase(TestCase):
    '''
    Base test case to be used in all `reply_idea` view tests
    '''
    def setUp(self):
        self.board = Discipline.objects.create(name='Test', description='Test Description')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.idea = Idea.objects.create(subject='This is a test idea', board=self.board, starter=user)
        Post.objects.create(message='This is a test post', idea=self.idea, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})

#class LoginRequiredReplyIdeaTests(ReplyIdeaTestCase):
    # ...

#class ReplyIdeaTests(ReplyIdeaTestCase):
    # ...

#class SuccessfulReplyIdeaTests(ReplyIdeaTestCase):
    # ...

#class InvalidReplyIdeaTests(ReplyIdeaTestCase):
    # ...