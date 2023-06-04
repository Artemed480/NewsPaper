from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        posts = Post.objects.filter(autor_id=self.author_user.id).values('rating')
        for post in posts:
            posts_rating += post['rating']

        comments_rating = 0
        author_comments = Comment.objects.filter(comment_user_id=self.author_user.id).values('rating')
        for comment in author_comments:
            comments_rating += comment['rating']

        post_comments_rating = 0
        post_comments = Comment.objects.filter(comment_user_id=self.author_user.id).values('rating')
        for comment in post_comments:
            post_comments_rating += comment['rating']

        self.author_rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPE = [(ARTICLE, 'Статья'), (NEWS, 'Новость')]

    autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE)
    post_data_time = models.DateTimeField(auto_now_add=True)
    post_categories = models.ManyToManyField(Category, through="PostCategory")
    post_title = models.TextField()
    post_text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + '...'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_data_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
