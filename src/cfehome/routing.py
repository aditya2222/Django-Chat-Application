from django.conf.urls import url  # We can use re_path as well
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({

    # Empty for now (http-->Django views, is added by default) 

    'websocket': AllowedHostsOriginValidator(

        AuthMiddlewareStack(

            URLRouter(

                [

                    url(r"^messages/(?P<username>[\w.@+-]+)", ChatConsumer),

                ]

            )

        )

    )
})
