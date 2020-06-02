from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..decorators import kinder_required
from ..models import *
from ..forms import *


class KinderSignUpView(CreateView):
    model = User
    form_class = KinderSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'kinder'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('kinders:viewpa')

@login_required
def viewki(request):
    tutors = Tutor.objects.all()
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    return render(request, 'classroom/kinders/index.html', {'tutors':tutors,'posts': posts})
