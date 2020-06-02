from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *

from ..forms import *
from django.db import transaction
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

from django.contrib import messages

def bevalide(request):
    return render(request, 'classroom/bevalide.html')

class TutorListView(ListView):
    model = User
    context_object_name = 'profs'

    def get_queryset(self):
        profs = User.objects.filter(user=self.request.user.teacher)
        paginator = Paginator(profs, 10)
        page = self.request.GET.get('page')
        try:
            profs = paginator.page(page)
        except PageNotAnInteger:
            profs = paginator.page(1)
        except EmptyPage:
            profs = paginator.page(paginator.num_pages)
        return profs

def profile(request):
    return render(request, 'classroom/profile.html')

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'classroom/profile_update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'votre profile est mise-a-jour')
            return HttpResponseRedirect(reverse_lazy('profile'))

            context = self.get_context_data(
                user_form=user_form,
                profile_form=profile_form
                )

            return self.render_to_response(context)     

            def get(self, request, *args, **kwargs):
                return self.post(request, *args, **kwargs)

def contact(request):
    return render(request, 'classroom/contact.html')

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:viewp')
        if request.user.is_kinder:
        	return redirect('kinders:viewki')
        if request.user.is_student:
            return redirect('students:viewe')
        else:
            return redirect('bevalide')
    return render(request, 'classroom/index.html', {})

@login_required
def post_list(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'paginate': True
    }
    return render(request, 'classroom/blog.html', {'posts': posts})

@login_required
def post_detail(request, year, month, day, post):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    # posts = posts.page(1)

    post = get_object_or_404(Post, slug=post)
    comments = post.comments.filter(active=True)
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    context = {
        'comments': comments,
        'paginate': True
    }
    print (comments)
    # for comment in comments:
    #   for reply in comment.replies.all():
    #       print reply.body
    #       # print reply.__dict__

    # rpy = Comment.objects.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,'classroom/post_detail.html',
        {'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'posts': posts
        })

