from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
#from django.contrib.auth import authenticate, login                               
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from chats.models import Message 
from listings.models import Listing, TuitionSession       
from users.models import Profile                                        
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
def message_list(request, sender=None, receiver=None, listingID=None):
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

# View Chat History
def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        h_list = get_history_list(request,Message.objects.all(),Listing.objects.all())
        return render(request, 'chat/chat_history.html', 
                      {'users': User.objects.exclude(username=request.user.username), #Returning context for all users except the current logged-in user
					  'listings': Listing.objects.all(),
					  'history_list': h_list}) 

# Function to get history list
def get_history_list(request, messages, listings):
	h_list = []
	for message in messages:
		for listing in listings:
			if listing.listingID == message.listingID.pk:

				if message.receiver_id == request.user.id:
					value1 = [int(request.user.id) , int(message.sender_id) , int(message.listingID.pk)]
					if value1 not in h_list:
						h_list.append(value1)
				elif message.sender_id == request.user.id:
					value1 = [int(request.user.id), int(message.receiver_id) , int(message.listingID.pk)]
					if value1 not in h_list:
						h_list.append(value1)
	return h_list						
						
# View to render template for sending and receiving messages	
# Takes arguments 'listingID' ,'sender' and 'receiver' to identify the message list to return
def message_listing_view(request, sender, receiver, listingID): 
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    else:
        # identify tutor and tutee
        obj = Listing.objects.get(listingID=listingID) #listingID
        listType = obj.typeOfListing
        #print(obj)
        tutor =""
        tutee =""
        tutorID = ""
        tuteeID = ""

        sender_name = Profile.objects.get(user_id=sender)
        receiver_name = Profile.objects.get(user_id=receiver)
        #print(receiver_name)

        if listType == "providing": #Listing host is learner
            #print(obj.user)
            tutee = obj.user
            #compare sender and receiver, whatever is not tutee must be the tutor
            if tutee != sender_name:
                tutor = sender_name
                tutorID = sender
                tuteeID = receiver
            else :
                tutor = receiver_name
                tutorID = receiver
                tuteeID = sender
        else : #listing host is teacher
            tutor = obj.user
            if tutor != sender_name:
                tutee = sender_name
                tuteeID = sender        
                tutorID = receiver
            else :
                tutee = receiver_name
                tuteeID = receiver
                tutorID = sender
        #print(obj)
        #print(tutorID)
        #print(tuteeID)

        tuitionSession, created = TuitionSession.objects.get_or_create(tutor=tutor, learner=tutee, listing=obj)
        #TuitionSession.objects.get(tutor=tutor, learner=tutee, listing=obj).offer
        #print(tuitionSession.offer)
        #print(tuitionSession)

        listings = Listing.objects.get(listingID = listingID)
        
        
        context = {
            'listing_id' : listingID,
		    'users': User.objects.exclude(username=request.user.username), #List of users
            'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
            'messages': Message.objects.filter(listingID=listingID,sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(listingID=listingID,sender_id=receiver, receiver_id=sender), # Return context with message objects where users are either sender or receiver.
			'listing': listings,
            'tuitionSession': tuitionSession,
            'user' : Profile.objects.get(user=request.user.id),
            'tutorID': tutorID,
            'receiverID' : receiver,
        }

        if request.method == "GET":
             return render(request, "chat/chat.html", context = context) 
        elif request.method == "POST":
            if request.POST.get("startSession"):
                tuitionSession.offer = 1 
                tuitionSession.save()
                context['tuitionSession'] = 1
                return render(request, "chat/chat.html", context=context)        
            elif request.POST.get("acceptSession"):
                tuitionSession.offer = 2 
                tuitionSession.save()
                context['tuitionSession'] = 2
                return render(request, "chat/chat.html", context=context)
            elif request.POST.get("completeSession"):
                tuitionSession.offer = 3 
                context['tuitionSession'] = 3
                tuitionSession.completed = True
                tuitionSession.save()
                return render(request, "chat/chat.html", context=context)
            #if request.POST.get("reviewSession"):
            #     tuitionSession.offer = 4 
            #     tuitionSession.save()
            #     context['tuitionSession'] = 4
            #    return render(request, "chat/chat.html", context=context)



	
def message_view(request, sender, receiver): 
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) | 
								   Message.objects.filter(sender_id=receiver, receiver_id=sender)})
