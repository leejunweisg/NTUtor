from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import profile, want_verified, UpdateProfile

# for profile pics
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('profile/<str:username>/', profile, name = 'profile'),
	path('edit-profile/', UpdateProfile, name = 'edit-profile'),
	path('want-verified/', want_verified, name='want-verified'),
]

# for profile pics
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)