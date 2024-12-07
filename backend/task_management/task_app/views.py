from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from .serializers import *

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

@permission_classes((AllowAny,))
class LoginViewSet(ViewSet):
    def create(self, request):
        try:
            user = authenticate(request, username=request.data['username'], password=request.data['password'])
            if not user:
                return Response({"status": "failed", 'message': 'invalid credentials'}, 401)
            token = generate_jwt_token(user)
            return Response(
                    {"status": "success", "message": "login successful", "user_id": user.id, "token":token})
        except Exception as e:
            return Response({"status": "failed", 'message': str(e)}, 500)
        
        
@permission_classes((AllowAny,))
class RegisterViewSet(ViewSet):
    # create user
    def create(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"status": "failed", 'message': serializer.errors}, 422)
            serializer.save()
            return Response({'message': 'record Saved successfully', 'data': serializer.data}, 200)
        except Exception as e:
            return Response({"status": "failed", 'message': str(e)}, 500)
