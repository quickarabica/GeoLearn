from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
class event1(models.Model):
    name=models.CharField(max_length=50)    
    email=models.EmailField()
    

    def __str__(self):
        return f"{self.name}-{self.email}"

class event2(models.Model):
    name=models.CharField(max_length=50)    
    email=models.EmailField()

    def __str__(self):
        return f"{self.name}-{self.email}"    
    
class contact(models.Model):
     name = models.ForeignKey(User, on_delete=models.CASCADE)  
    
     message=models.TextField()

     def __str__(self):
        return f"{self.name}-{self.message}"