"""cjapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from api.v1.friendship.views import FriendshipView, FriendsView, FriendSuggestionsView
from api.v1.users.views import UserCreateView
from restapi.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('suggestions/<for_user>', FriendSuggestionsView.as_view(), name="get_suggested_friends"),
    path('api/', include(('api.urls', "api"), namespace="api")),
    path('create', UserCreateView.as_view(), name="create_user"),
    path('add/<from_user>/<to_user>', FriendshipView.as_view(), name="add_friends"),
    path('friendRequests/<to_user>', FriendshipView.as_view(), name="get_pending_requests"),
    path('friends/<to_user>', FriendsView.as_view(), name="get_friends"),

    url(r'', index),
]
