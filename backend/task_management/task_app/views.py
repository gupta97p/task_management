from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ViewSet

from .models import Task, userReg
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


class TaskViewSet(ViewSet):

    def list(self, request):
        user = userReg.objects.get(id=request.user.id)
        queryset = Task.objects.filter(user=user, is_active=True)

        # Serialize the filtered queryset
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
                return Response({'status': 'failed', 'data': {'message': serializer.errors}}, 422)
        serializer.save()
        return Response({"data": serializer.data}, 200)

    def patch(self, request, pk=None):
        task_obj = Task.objects.get(id=pk)
        if task_obj:
            serializer = TaskSerializer(task_obj, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 'failed', 'data': {"message": serializer.errors}}, 422)
            serializer.save()
            return Response({"message": "Task updated succesfully"}, 200)
        else:
            return Response({"message": f"Task with id {pk} not found"}, 400)
        
    def destroy(self, request, pk=None):
        try:
            task_obj = Task.objects.get(pk=pk)
            if task_obj:
                task_obj.is_active = False
                task_obj.save()
            else:
                return Response({"message": f"Task with id {pk} not found"}, 400)
        except Exception as e:
            return Response('some exception occurred ' + str(e), 500)
        return Response('record Deleted successfully', 200)