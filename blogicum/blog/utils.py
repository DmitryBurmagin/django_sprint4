from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_unfiltred_post():
    return Post.objects.select_related(
        'author',
        'category',
        'location',
    ).order_by(
        '-pub_date'
    ).annotate(comment_count=Count('comments'))


def filter_published_posts(queryset):
    return queryset.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
