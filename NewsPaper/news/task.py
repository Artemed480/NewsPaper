from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from news.signals import notify_subscriber
from .models import Post, PostCategory, Category, Subscription
from django.template.loader import render_to_string
from NewsPaper import settings
import datetime


@shared_task
def send_notifications(pk):
    post = Post.objects.get(pk=pk)
    categories = Post.post_categories.all()
    title = Post.post_title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_users in subscribers_users:
            subscribers_emails.append(sub_users.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text':post.preview(),
            'link':f'{settings.SITE_URL}/news/pk'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def send_mail():
    for category in Category.objects.all():
        subscribers = list(Subscription.objects.filter(category=category).values_list('user__email', flat=True))
        posts_list = list(category.record_set.filter(date__gte=datetime.utcnow() - datetime.timedelta(days=7)))

        for email in subscribers:

            html_content = render_to_string(
                'subscribe/week_posts.html',
                {
                    'posts_list':posts_list,
                    'link': settings.SITE_URL,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()