from django.views.generic import (
    UpdateView, DeleteView, CreateView, ListView, DetailView)
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404

from .models import Post, Category, User, Comment
from .forms import (
    PostForm, UserUpdateForm, CommentsForm, CommentsEditForm
)


POST_PER_PAGE = 10


def get_queryset():
    return Post.objects.select_related(
        'author',
        'category',
        'location',
    ).order_by(
        '-pub_date'
    ).annotate(comment_count=Count('comments'))


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class CommentMixin:
    model = Comment
    form_class = CommentsEditForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


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
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class IndexViewList(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        return get_queryset().filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True)


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
            from_email='ADMIN@ADMINOV.RU',
            recipient_list=[self.request.user.email]
        )


class BlogPostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if not post.is_published and post.author != self.request.user:
            raise Http404("Пост не найден")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = self.object.comments.all(
        ).order_by('created_at').select_related('author')
        return context


class BlogPostEdit(LoginRequiredMixin, PostMixin, UpdateView):

    def dispatch(self, request, *args, **kwargs):
        post = super().get_object()
        if post.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})


class BlogPostDelete(LoginRequiredMixin, PostMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        post = super().get_object()
        if post.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

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


class BlogCommentDelete(LoginRequiredMixin, CommentMixin, DeleteView):

    def dispatch(self, request, *args, **kwargs):
        comment = super().get_object()
        if comment.author != self.request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        return get_queryset().filter(
            author__username=self.kwargs['username']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.kwargs['username']}
        )
