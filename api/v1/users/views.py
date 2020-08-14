from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.users.serializers import UserSerializer


class UserCreateView(APIView):
    """
    Creates the user.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"username": user.username}, status=status.HTTP_201_CREATED)

        return Response({"status": "failure", "reason": "any string"}, status=status.HTTP_400_BAD_REQUEST)
