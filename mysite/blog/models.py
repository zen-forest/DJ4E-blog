from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

  class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250)

  # One to many relationship
  # Django will create a foreign key in the database using the primary key of the related model 
  # on_delete specifies behavior which is a SQL standard, using CASCADE you specify when the user is deleted, thte db will delete all blog posts
  # related_name is essentially a backlink that will be viewed from the user object 
  author = models.ForeignKey(User,on_delete=models.CASCADE, 
                             related_name='blog_posts')

  body = models.TextField()
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, 
                            choices=Status.choices, 
                            default=Status.DRAFT)

  objects = models.Manager()
  published = PublishedManager()

  # This class defines the metadata for the model 
  # This will apply a default ordering 
  class Meta: 
    ordering = ['-publish']
    indexes = [
      models.Index(fields=['-publish']),
    ]

  def __str__(self):
    return self.title 