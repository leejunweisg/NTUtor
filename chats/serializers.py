from django.contrib.auth.models import User
from rest_framework import serializers #make use of Serializer class
from chats.models import Message
from listings.models import Listing
 
# User Serializer
class UserSerializer(serializers.ModelSerializer):
	#To avoid displaying password on GET request
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']
 
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
	#listingID = serializers.SlugRelatedField(many=False, slug_field='listingID', queryset=Listing.objects.all())
	# Message only has one sender and receiver
	sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
	class Meta:
		model = Message
		fields = ['listingID','sender', 'receiver', 'message', 'timestamp']