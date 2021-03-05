from django.db import models
from listings.models import Listing
#from users.models import Profile
from django.contrib.auth.models import User

# TODO: Chat Model

# class Chat(models.Model):
#     chatID = models.AutoField(primary_key=True)
#     listingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     tutor = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="tutor")
#     learner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name="learner")

#     def __str__(self):
#         return f"{self.chatID}"

class Message(models.Model):
	#identify post
	listingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
	#identify sender of message
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	#identify receiver of message
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver') 
	#store message text
	message = models.CharField(max_length=1200)
	#stores date and time of creation of message
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.message
	class Meta:
		#Order message by timestamp for front-end purpose
		ordering = ('timestamp',)
