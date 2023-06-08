from django_filters import FilterSet
from news.models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_data_time': ['date__gte'],
            'autor': ['exact'],
        }
