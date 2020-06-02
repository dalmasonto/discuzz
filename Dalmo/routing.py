from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from my_app.consumers import SendEmailConsumer, SendReplyConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path('emails/', SendEmailConsumer),
                    path('discuzz/<str:discussion_Code>/', SendReplyConsumer),
                ]
            )
        )
    )
})
