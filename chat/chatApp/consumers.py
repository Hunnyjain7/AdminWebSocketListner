import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.sessions.models import Session
from .models import UserRole, Role

admin_session_id = None


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    def connect(self):
        global admin_session_id

        session_id = self.scope['cookies']['sessionid']
        self.room_group_name = session_id

        session = Session.objects.get(session_key=self.room_group_name)
        user_id = session.get_decoded().get('id')
        obj = UserRole.objects.get(user_id=user_id).role_id
        role = Role.objects.get(id=obj.id)
        if role.role_name == 'Admin':
            admin_session_id = self.room_group_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'status': 'connected'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if admin_session_id is not None:
            print("not None")
            async_to_sync(self.channel_layer.group_send)(
                admin_session_id,
                {
                    'type': 'chat_message',
                    'message': message
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



