from django.db import models
from users.models import Profile
from listings.models import TuitionSession
from django.utils import timezone

from django.urls import reverse
from django.shortcuts import redirect


class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)

    # Set the tuition session to null, but leave review there
    tuitionSession = models.ForeignKey(TuitionSession,related_name="tuitionSession", on_delete = models.SET_NULL, null=True)
    #date_posted = models.DateTimeField(default=timezone.now)
    reviewee = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="reviewee", null=True)
    reviewer = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="reviewer", null=True)
    description = models.TextField(max_length=3000)

    # Need to create validation either on form side or model side
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.reviewID}"

    def get_absolute_url(self):
         return reverse('reviews-username',kwargs={'tutorid':self.reviewee_id})
       
        

   