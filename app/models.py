from django.db import models
from django.db.models.expressions import F
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField





class Post(models.Model):
    
    promote = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    viewers = models.IntegerField(default=0, blank=True, null=True)
    title = models.CharField(max_length=100, unique=True, null=True, blank=False)
    title2 = models.CharField(max_length=200, blank=False, null=True)
    text = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = "images/", default='default.jpg')
    details = RichTextField(blank=False, null=True)
    

    def __str__(self):
        return self.title
     

    def get_absolute_url(self):
        return  reverse("Edame_Akhbar", kwargs={"id": self.id})     
    
      
      
      
       
        
class Comment(models.Model):
    
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)        
        
 