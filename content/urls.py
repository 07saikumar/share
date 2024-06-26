from django.contrib import admin
from django.urls import path
from content import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('create/', views.create_room, name='create_room'),
    path('public/', views.public_section, name='public_section'),
    path('rooms/', views.access_room, name='access_room'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/messages/', views.fetch_messages, name='fetch_messages'),
    path('public/messages/', views.fetch_public_messages, name='fetch_public_messages'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)