from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from news.models import Post, Category, PostCategory, User, Author, Subscription
from news.forms import PostForm
from news.filters import PostFilter
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, reverse, redirect


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-post_data_time'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def get_context_data2(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_common'] = not self.request.user.groups.filter(name='common').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = '-post_data_time'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'create.html'
    permission_required = ('news.add_post',)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'update.html'
    permission_required = ('news.change_post',)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class PostCategoryView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'posts'
    ordering = '-post_data_time'
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        queryset = Post.objects.filter(post_categories=Category.objects.get(id=self.id))
        return queryset

    def get_context_data1(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fiter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['category'] = Category.objects.get(id=self.id)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        context['category'] = category
        if subscribed:
            context['subscribed'] = 1
        return context


@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if not cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.add(user)
        html = render_to_string(
            'subscribe/subscribed.html',
            {'category' : cat, 'user' : user}
        )
        category = f'{cat}'
        email = user.email
        msg = EmailMultiAlternatives(
            subject=f'{category} category subscription',
            from_email='mednikoffartem@yandex.ru',
            body='',
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)

    if cat.subscribers.filter(id=user.id).exists():
        cat.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))