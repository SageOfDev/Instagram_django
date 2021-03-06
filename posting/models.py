from django.db import models
from user.models import User


class Posting(models.Model):
    content = models.CharField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'


class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'comments'


class Like(models.Model):
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'