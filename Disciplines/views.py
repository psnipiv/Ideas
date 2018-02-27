from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .forms import NewIdeaForm, PostForm
from .models import Discipline,Idea,Post
# Create your views here.

@method_decorator(login_required, name='dispatch')
class DisciplineListView(ListView):
    model = Discipline
    context_object_name = 'disciplines'
    template_name = 'home.html'

@method_decorator(login_required, name='dispatch')
class IdeaListView(ListView):
    model = Idea
    context_object_name = 'ideas'
    template_name = 'ideas.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['discipline'] = self.discipline
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.discipline = get_object_or_404(Discipline, pk=self.kwargs.get('pk'))
        queryset = self.discipline.ideas.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'idea_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_idea_{}'.format(self.idea.pk)
        if not self.request.session.get(session_key, False):
            self.idea.views += 1
            self.idea.save()
            self.request.session[session_key] = True
        kwargs['idea'] = self.idea
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.idea = get_object_or_404(Idea, discipline__pk=self.kwargs.get('pk'), pk=self.kwargs.get('idea_pk'))
        queryset = self.idea.posts.order_by('created_at')
        return queryset


@login_required
def new_idea(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.discipline = discipline
            idea.starter = request.user
            idea.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                idea=idea,
                created_by=request.user
            )
            return redirect('discipline_ideas', pk=discipline.pk)  # TODO: redirect to the created idea page
    else:
        form = NewIdeaForm()

    return render(request, 'new_idea.html', {'discipline' : discipline,'form' : form})

@login_required
def reply_idea(request, pk, idea_pk):
    idea = get_object_or_404(Idea, discipline__pk=pk, pk=idea_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.idea = idea
            post.created_by = request.user
            post.save()

            idea.last_updated = timezone.now()
            idea.save()

            idea_url = reverse('idea_posts', kwargs={'pk': pk, 'idea_pk': idea_pk})
            idea_post_url = '{url}?page={page}#{id}'.format(
                url=idea_url,
                id=post.pk,
                page=idea.get_page_count()
            )

            return redirect(idea_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_idea.html', {'idea': idea, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('idea_posts', pk=post.idea.discipline.pk, idea_pk=post.idea.pk)