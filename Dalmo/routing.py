from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from my_app.consumers import SendEmailConsumer, SendReplyConsumer, MyAdminConsumer
from inbox.consumers import SendMessageConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('emails/', SendEmailConsumer),
                    path('discuzz/<str:discussion_Code>/', SendReplyConsumer),
                    path('myadmin/', SendReplyConsumer),
                    path('chat/<str:username>/', SendMessageConsumer),
                ]
            )
        )
    )
})
