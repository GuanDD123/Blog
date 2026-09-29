from django.contrib import admin

from chat.models import ChatRoom, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "display_users")
    search_fields = ("name",)
    inlines = (MessageInline,)
    readonly_fields = ("display_users",)

    @admin.display(description="Users")
    def display_users(self, obj):
        return ", ".join(user.username for user in obj.users.all())


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sent_on", "user", "chat_room", "content")
    list_filter = ("sent_on", "chat_room")
    search_fields = ("content",)
    autocomplete_fields = ("user", "chat_room")
