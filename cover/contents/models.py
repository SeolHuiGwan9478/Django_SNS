from django.db import models
from django.contrib.auth.models import User
import os, uuid
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    text = models.TextField(verbose_name='글 내용',default='')

    class Meta:
        ordering = ['-created_at']

def image_upload_to(instance, filename):
    ext = filename.split('.')[-1] #확장자
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))

class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField()

    class Meta:
        unique_together = ['content', 'order']
        ordering = ['order']

class FollowRelation(BaseModel):
    follower = models.OneToOneField(User, related_name='follower', on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='followee')