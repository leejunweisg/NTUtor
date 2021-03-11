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
        # Offer has not been given, offer = -1
        # Waiting to accept offer:
        # If offer made by other person, offer = 0. 
        # If offer made by yourself, offer = 1
        # If offer accepted, offer = 2
        # Session completed, offer = 3

        # Do methods to get TuitionSession and if it exists, check initatedOffer and acceptOffer
        # If initiated by ownself, and acceptOffer = 0, means context['offer'] = 1, else context['offer] = 0
        # if acceptOffer = 1, context['offer'] = 2
        # if completed = True, context['offer'] = 3
        # If TuitionSession does not exist, context['offer'] = -1 
        

        listings = Listing.objects.get(listingID = listingID)
        context = {
            'listing_id' : listingID,
		    'users': User.objects.exclude(username=request.user.username), #List of users
            'receiver': User.objects.get(id=receiver), # Receiver context user object for using in template
            'messages': Message.objects.filter(listingID=listingID,sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(listingID=listingID,sender_id=receiver, receiver_id=sender), # Return context with message objects where users are either sender or receiver.
			'listing': listings
        }

        if request.method == "GET":
             return render(request, "chat/chat.html", context = context) 
        elif request.method == "POST":
            if request.POST.get("startSession"):
                # Change context
                obj = Listing.objects.get(listingID=listingID) #listingID
                listType = obj.typeOfListing
                #print(obj)
                tutor =""
                tutee =""
                tutorID = ""
                tuteeID = ""

                sender_name = Profile.objects.get(user_id=sender)
                receiver_name = Profile.objects.get(user_id=receiver)

                if listType == "providing": #Listing host is learner
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
                print(listingID)
                print(tutorID)
                print(tuteeID)
                #tuitionSession = TuitionSession.objects.all()
                #print(tuitionSession)
                
                you = User.objects.filter(username=request.user.username)
                #you1 = Profile.objects.filter(you.username)
                tuitionSession, created = TuitionSession.objects.get_or_create(tutor=tutor, learner=tutee, listing=obj)
                return HttpResponse("<h1>Send Offer</h1>")
                #context['offer'] = 0

        #         # Create tuition session


        #     if request.POST.get("acceptSession"):
        #         # Change context
        #         context['offer'] = 1
                
        #         # Update database acceptOffer to 1


        #     if request.POST.get("completeSession"):
        #         # Change context
        #         context['offer'] = 2

        #         # Update database completed = True

                
        #     return render(request, "chat/chat.html", context = context) """



	
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

#Send offer test
def test_view(request, sender, receiver, listingID):
    #TuitionSessionQuery = request.GET.get('sendOffer')

    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        obj = Listing.objects.get(listingID=listingID)
        listType = obj.typeOfListing
        #print(obj)
        tutor =""
        tutee =""
        tutorID = ""
        tuteeID = ""

        sender_name = Profile.objects.get(user_id=sender)
        receiver_name = Profile.objects.get(user_id=receiver)

        if listType == "providing": #Listing host is learner
            tutee = obj.user
            #compare sender and receiver, whatever is not tutee must be the tutor
            if tutee != sender_name:
               #tutor = sender_name
                tutorID = sender
                tuteeID = receiver
            else :
                #tutor = receiver_name
                tutorID = receiver
                tuteeID = sender
        else : #listing host is teacher
            tutor = obj.user
            if tutor != sender_name:
                #tutee = sender_name
                tuteeID = sender
                tutorID = receiver
            else :
                #tutee = receiver_name
                tuteeID = receiver
                tutorID = sender
        print(tutorID)
        print(tuteeID)
        tuitionSession, created = TuitionSession.objects.get_or_create(tutor_id=tutorID, learner_id=tuteeID, listing_id=listingID)
        return HttpResponse("<h1>Send Offer</h1>")
        

        # {% csrf_token %}
		# 				{{ if offer == 0}}
		# 					<button class="btn btn-primary"type="submit" name="startSession" id="startSession" value="startSession">Make offer to start tuition session</button>
		# 				{{ elif offer == 1 }}
		# 					<button class="btn btn-primary"type="submit" name="acceptSession" id="acceptSession" value="acceptSession">Accept tuition session</button>	
		# 				{{ elif offer == 2 }}
		# 					<p> Waiting for other student to accept </p>
		# 				{{ elif offer == 3 }}
		# 					<button class="btn btn-primary"type="submit" name="completeSession" id="completeSession" value="completeSession">Complete session</button>
		# 				{{ elif offer == 4}}
		# 					<!-- Link to leave review -->
						
		# 				{{ endif }}