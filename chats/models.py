from django.db import models
from listings.models import Listing
from users.models import Profile

#Chat may not need model? Will look into it
#Actual chat text may be stored elsewhere?

class Chat(models.Model):
    chatID = models.AutoField(primary_key=True)
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="tutor")
    learner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="learner"

    def __str__(self):
        return f"{self.chatID}"


