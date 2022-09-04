import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.sessions.models import Session
from .models import UserRole, Role, User


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.user_id = None

    def connect(self):
        session_id = self.scope['cookies']['sessionid']  # noqa
        session = Session.objects.get(session_key=session_id)
        user_id = session.get_decoded().get('id')

        self.room_group_name = str(user_id)
        self.user_id = user_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'status': 'connected'
        }))

    def receive(self, text_data): # noqa
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        name = User.objects.get(id=self.user_id).name

        admins = UserRole.admins()
        for admin in admins:
            async_to_sync(self.channel_layer.group_send)(
                str(admin.id),
                {
                    'type': 'chat_message',
                    'message': name + ': ' + message
                }
            )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
