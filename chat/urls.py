from django.urls import path

from .views import chat

app_name = "chat"
urlpatterns = [
    path("room/<int:room_pk>/", chat, name="chat_room"),
]
