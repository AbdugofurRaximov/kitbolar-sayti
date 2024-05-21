from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from .settings import MEDIA_URL, MEDIA_ROOT
from .views import landing_page,home_page
from django.conf.urls.static import static
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path("home/", home_page, name='home_page'),
    path("users/", include('users.urls')),
    path("books/", include('books.urls')),
    path("api/", include('api.urls')),
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),



]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
