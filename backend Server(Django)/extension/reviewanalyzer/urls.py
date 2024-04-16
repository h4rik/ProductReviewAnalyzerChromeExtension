from django.contrib import admin
from django.urls import path, include  # Import includefrom .views import send_email
from .views import send_email


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reviewanalyzer/', include('reviewanalyzer.urls')),  # Assuming you have a urls.py in your app
    path('send_email/', send_email, name='send_email'),
]



