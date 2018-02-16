from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Discipline,Idea,Post
from django.contrib.auth.decorators import login_required
from .forms import NewIdeaForm
from .forms import PostForm
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone



# Create your views here.

@login_required
def home(request):
    disciplines = Discipline.objects.all()
    return render(request, 'home.html', {'disciplines': disciplines})

@login_required
def discipline_ideas(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    ideas = discipline.ideas.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'ideas.html', {'discipline': discipline,'ideas': ideas})

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


def idea_posts(request, pk, idea_pk):
    idea = get_object_or_404(Idea, discipline__pk=pk, pk=idea_pk)
    idea.views += 1
    idea.save()
    return render(request, 'idea_posts.html', {'idea': idea})

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
            return redirect('idea_posts', pk=pk, idea_pk=idea_pk)
    else:
        form = PostForm()
    return render(request, 'reply_idea.html', {'idea': idea, 'form': form})


class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('idea_posts', pk=post.idea.discipline.pk, idea_pk=post.idea.pk)