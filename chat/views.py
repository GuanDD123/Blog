from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ChatRoom


@login_required
def chat(request, room_pk):
    chat_room, _ = ChatRoom.objects.get_or_create(
        pk=room_pk, name=f"Chat Room {room_pk}"
    )
    if request.user not in chat_room.users.all():
        chat_room.users.add(request.user)

    latest_messages = reversed(
        chat_room.chat_messages.select_related("user").order_by("-id")[:5]
    )
    return render(
        request,
        "chat/room.html",
        {"chat_room": chat_room, "latest_messages": latest_messages},
    )
