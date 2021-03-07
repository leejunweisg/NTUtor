from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
#from django.contrib.auth import authenticate, login                               
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from chats.models import Message 
from listings.models import Listing                                                 
from chats.serializers import MessageSerializer, UserSerializer 
 

# Views to return our serialized data 
# Users View
@csrf_exempt                                                              
def user_list(request, pk=None):

    if request.method == 'GET':
        if pk:                                                                      
		# If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            users = User.objects.all()                             # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request}) 
        return JsonResponse(serializer.data, safe=False)               # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)        # Serialize the data
        if serializer.is_valid():
            serializer.save()                                            # Save if valid
            return JsonResponse(serializer.data, status=201)     # Return back the data on success
        return JsonResponse(serializer.errors, status=400)     # Return back the errors  if not valid

# Message View
@csrf_exempt
def message_list(request, sender=None, receiver=4, listingID=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
		#Requires sender, receiver, listingID as URL parameters
        messages = Message.objects.filter(listingID=listingID,sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        print("GET serializer:",serializer)		
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = MessageSerializer(data=data)
        print("serializer:",serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# View Listing the Users
# Change to only history of users...(Function to be edited again)
def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        #print("chat.html")
        return render(request, 'chat/chat_history.html', 
                      {'users': User.objects.exclude(username=request.user.username), #Returning context for all users except the current logged-in user
					  'messages': Message.objects.filter(message__isnull=False),
					  'listing': Listing.objects.all()}) 

# TO be removed in future...			
def message_view(request, sender, receiver): 
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
		#print("messages.html")
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) | 
								   Message.objects.filter(sender_id=receiver, receiver_id=sender)}) 
								  
								   
# View to render template for sending and receiving messages	
# Takes arguments 'listingID' ,'sender' and 'receiver' to identify the message list to return
def message_listing_view(request, sender, receiver, listingID): 
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
       # print("messages.html")
        return render(request, "chat/chat.html",
                      {'listing_id' : listingID,
					   'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(listingID=listingID,sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(listingID=listingID,sender_id=receiver, receiver_id=sender), # Return context with message objects where users are either sender or receiver.
						'listing': Listing.objects.get(listingID = listingID)}) 