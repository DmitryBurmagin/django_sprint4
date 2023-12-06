from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.IndexViewList.as_view(),
        name='index'
    ),
    path(
        'posts/<int:post_id>/',
        views.BlogPostDetail.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.BlogPostEdit.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.BlogPostDelete.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.BlogCommentAdd.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.BlogCommentEdit.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.BlogCommentDelete.as_view(),
        name='delete_comment'
    ),
    path(
        'category/<str:category_slug>/',
        views.BlogCategoryPosts.as_view(),
        name='category_posts'
    ),
    path(
        'posts/create/',
        views.BlogCreateView.as_view(),
        name='create_post'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'profile/<str:username>/edit/',
        views.ProfileEditView.as_view(),
        name='edit_profile'
    ),
]
