# """
# ASGI config for CScommunity project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
# """

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
import chatting.routing
# from channels.security.websocket import AllowedHostsOriginValidator
# from chat import consumers
# import chat.chat.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CScommunity.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatting.routing.websocket_urlpatterns
        )
    )
})

# application = ProtocolTypeRouter({
#               'http':get_asgi_application(),
#     'websocket':URLRouter(
#            chat.chat.routing.websocket_urlpatterns
#     )
# })
# #     AuthMiddlewareStack(
# #         AllowedHostsOriginValidator(
# #             URLRouter(
# #                 [
# #                    path('ws/pc/',consumers.PublicChat.as_asgi())
# #                 ]
# #             )
# #         )
# #     )
# # })

# # application = get_asgi_application()
# # import os








