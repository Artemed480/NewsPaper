# Generated by Django 4.2.1 on 2023-06-04 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_rating', models.IntegerField(default=0)),
                ('author_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='AR', max_length=2)),
                ('post_data_time', models.DateTimeField(auto_now_add=True)),
                ('post_title', models.TextField()),
                ('post_text', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post_through', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_categories',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('comment_data_time', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
