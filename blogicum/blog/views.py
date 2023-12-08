from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blogicum.settings import EMAIL_ADRESS

from .forms import CommentForm, UserUpdateForm
from .mixins import CommentDelMixin, CommentMixin, PostDelMixin, PostMixin
from .models import Category, Post, User
from .utils import filter_published_posts, get_unfiltred_post

POST_PER_PAGE = 10


class BlogCategoryPosts(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POST_PER_PAGE
    ordering = '-pub_date'

    def get_queryset(self):
        slug = self.kwargs['category_slug']
        self.category = get_object_or_404(
            Category,
            slug=slug,
            is_published=True
        )
        return super().get_queryset().filter(
            category=self.category,
            is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class IndexViewList(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        queryset = get_unfiltred_post()
        return filter_published_posts(queryset)


class BlogCreateView(LoginRequiredMixin, PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.mail()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user})

    def mail(self):
        send_mail(
            subject='Привет',
            message='Вы опубликоали пост',
            from_email=EMAIL_ADRESS,
            recipient_list=[self.request.user.email]
        )


class BlogPostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author != self.request.user:
            if any(
                [
                    post.pub_date >= timezone.now(),
                    not post.is_published,
                    not post.category.is_published,
                ]
            ):
                raise Http404("Пост не найден")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all(
        ).select_related('author')
        return context


class BlogPostEdit(LoginRequiredMixin, PostMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        post = super().get_object()
        if post.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})


class BlogPostDelete(LoginRequiredMixin, PostDelMixin, PostMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class BlogCommentAdd(LoginRequiredMixin, CommentMixin, CreateView):
    pass


class BlogCommentEdit(LoginRequiredMixin, CommentMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        comment = super().get_object()
        if comment.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class BlogCommentDelete(LoginRequiredMixin, CommentDelMixin, CommentMixin,
                        DeleteView):
    pass


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        if self.request.user.username == self.kwargs['username']:
            return get_unfiltred_post().filter(
                author__username=self.kwargs['username']
            )
        return get_unfiltred_post().filter(
            author__username=self.kwargs['username'],
            is_published=True,
            pub_date__lt=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user.username)

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})
