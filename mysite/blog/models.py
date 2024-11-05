from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
from django.urls import reverse
from django.conf import settings



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)
    


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish= models.DateTimeField(default=timezone.now)
    #publish= models.DateTimeField(db_default==Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.DRAFT
    )


    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()

    class Meta:
        ordering = ('-publish',)
        indexes=[
            models.Index(fields=['-publish']),
        ]
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                       args=[
                            self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug
                           ])

    def __str__(self):
        return self.title

