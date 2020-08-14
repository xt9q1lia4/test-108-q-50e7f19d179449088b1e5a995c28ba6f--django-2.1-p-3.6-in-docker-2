from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from friendship.models import Friend, FriendshipRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FriendshipView(APIView):
    def post(self, request, from_user, to_user, *args, **kwargs):
        try:
            from_user = User.objects.get(username=from_user)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(username=to_user)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pending_friendship_request = FriendshipRequest.objects.filter(to_user=from_user, from_user=to_user)
            if pending_friendship_request.exists():
                pending_friendship_request.first().accept()
                return Response({"status": "success"}, status=status.HTTP_202_ACCEPTED)
            if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
                return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)
            if to_user in Friend.objects.friends(from_user):
                return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)
            Friend.objects.add_friend(from_user, to_user, message='Hi! I would like to add you')
            return Response({"status": "success"}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, to_user, *args, **kwargs):
        try:
            user = User.objects.get(username=to_user)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

        pending_friendship_request = FriendshipRequest.objects.filter(to_user=user)

        if not pending_friendship_request.exists():
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"friend_requests": pending_friendship_request.values_list("from_user__username", flat=True)}, status=status.HTTP_200_OK)


class FriendsView(APIView):
    def get(self, request, to_user, *args, **kwargs):
        try:
            user = User.objects.get(username=to_user)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

        friends = Friend.objects.friends(user)

        if not friends:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"friends": [friend.username for friend in friends]}, status=status.HTTP_200_OK)


class FriendSuggestionsView(APIView):
    def get(self, request, for_user, *args, **kwargs):
        try:
            user = User.objects.get(username=for_user)
        except ObjectDoesNotExist as exception:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)

        friends = Friend.objects.filter(from_user=user)
        print("friends", friends.values_list("to_user__username", flat=True))

        first_degree_friends = Friend.objects.filter(
            from_user__friends__from_user=user
        ).exclude(to_user__username__in=friends.values_list("to_user__username", flat=True)
                  ).exclude(to_user__username=for_user).distinct().values_list("to_user__username", flat=True)
        second_degree_friends = Friend.objects.filter(
            from_user__friends__from_user__friends__from_user=user
        ).exclude(to_user__username__in=friends.values_list("to_user__username", flat=True)
                  ).exclude(to_user__username=for_user).distinct().values_list("to_user__username", flat=True)
        print("1st friends", first_degree_friends)
        print("2nd friends", second_degree_friends)
        suggestions = []
        suggestions.extend(first_degree_friends)
        suggestions.extend(second_degree_friends)

        if not suggestions:
            return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"suggestions": suggestions}, status=status.HTTP_200_OK)
