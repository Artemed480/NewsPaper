from django.urls import path
from news.views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, PostCategoryView, CategoryList
from news.views import subscribe_to_category, unsubscribe_from_category

app_name = 'news'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view()),
    path('search', PostSearch.as_view()),
    path('create/', PostCreate.as_view()),
    path('<int:pk>/update/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>', PostCategoryView.as_view(), name='category'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsubscribe'),
]