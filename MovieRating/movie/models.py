from django.db import models
from django.contrib.auth.models import User
# Create your modelss here.

CATEGORY_CHOICES = (
        ('action', 'Action'),
        ('love', 'Love'),
        ('sci-fi', 'Science Fiction'),
        # Add more categories as needed
    )

class Movie(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=250)
    year = models.DecimalField(decimal_places=1,max_digits=5,unique=False)
    description = models.TextField(unique=False)
    rating = models.FloatField(unique=False)
    vote_avg = models.FloatField(unique=False)
    img_url = models.CharField(max_length=250)
    category = models.CharField(max_length=250,unique=False,null=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):    
    text = models.CharField(max_length=100)    
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    watchAgain = models.BooleanField()    

    def __str__(self):
        return self.text
