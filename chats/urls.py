# Point to mainapp url
from django.urls import path
from . import views

urlpatterns = [
	# Messages: "/api/messages/4/3/1"
    path('api/messages/<int:sender>/<int:receiver>/<int:listingID>', views.message_list, name='message-detail'),  # For GET request.
    path('api/messages', views.message_list, name='message-list'),   # For POST
   
    # Users: "/api/users/1"
    path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('api/users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
	
	# Chat
	path('chat/', views.chat_view, name='chats'), # sample chat history template. To be linked to profile page.
	path('chat/<int:sender>/<int:receiver>/<int:listingID>', views.message_listing_view, name='chat'),
	path('chat/<int:sender>/<int:receiver>', views.message_view, name='chat'),
	
<<<<<<< Updated upstream
=======
    #for testing
    path('chat/<int:sender>/<int:receiver>/<int:listingID>',test_view, name='test-detail'),
>>>>>>> Stashed changes
]