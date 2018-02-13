from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Discipline,Idea,Post
from django.contrib.auth.decorators import login_required
from .forms import NewIdeaForm


# Create your views here.

@login_required
def home(request):
    disciplines = Discipline.objects.all()
    return render(request, 'home.html', {'disciplines': disciplines})

@login_required
def discipline_ideas(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    return render(request, 'ideas.html', {'discipline': discipline})

@login_required
def new_idea(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.discipline = discipline
            idea.starter = user
            idea.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                idea=idea,
                created_by=user
            )
            return redirect('discipline_ideas', pk=discipline.pk)  # TODO: redirect to the created idea page
    else:
        form = NewIdeaForm()

    return render(request, 'new_idea.html', {'discipline' : discipline,'form' : form})