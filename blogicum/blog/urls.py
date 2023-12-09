from django.urls import include, path

from . import views

app_name = 'blog'


post_urls = [
    path(
        '<int:post_id>/',
        views.BlogPostDetail.as_view(),
        name='post_detail'
    ),
    path(
        '<int:post_id>/edit/',
        views.BlogPostEdit.as_view(),
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.BlogPostDelete.as_view(),
        name='delete_post'
    ),
    path(
        '<int:post_id>/comment/',
        views.BlogCommentAdd.as_view(),
        name='add_comment'
    ),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        views.BlogCommentEdit.as_view(),
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        views.BlogCommentDelete.as_view(),
        name='delete_comment'
    ),
    path(
        'create/',
        views.BlogCreateView.as_view(),
        name='create_post'
    ),

]

urlpatterns = [
    path(
        '',
        views.IndexViewList.as_view(),
        name='index'
    ),
    path('posts/',
         include(post_urls)
         ),
    path(
        'category/<str:category_slug>/',
        views.BlogCategoryPosts.as_view(),
        name='category_posts'
    ),
    path(
        'profile/edit/',
        views.ProfileEditView.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
]
