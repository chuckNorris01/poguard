from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserLoginSerializer

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'expires_at': serializer.data['expires_at'],
                'expires_in': serializer.data['expires_in'],
                'UserInfo': {
                    'email': serializer.data['email'],
                    'name': serializer.data['name'], 
                    'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)
