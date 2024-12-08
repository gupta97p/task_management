from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Task, userReg
from .serializers import RegisterSerializer, TaskSerializer
from .filters import TaskFilter
from .pagination import CustomPagination

from django.shortcuts import get_object_or_404


def generate_jwt_token(user):
    """ Generates login token for the user

    Args:
        user (_type_): userReg

    Returns:
       access_token _type_: String 
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class LoginViewSet(ViewSet):
    permission_classes = [AllowAny]
    
    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if not username or not password:
            return Response({"status": "failed", "message": "Username and password are required"}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"status": "failed", 'message': 'invalid credentials'}, status=401)
        token = generate_jwt_token(user)
        return Response(
                {"status": "success", "message": "login successful", "user_id": user.id, "token":token}, status=200)
        

class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny]
    
    def create(self, request):
        """
            Function to create user/ Signup
        """
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "failed", 'message': serializer.errors}, status=422)
        serializer.save()
        return Response({"status": "success", 'message': 'Record Saved successfully', 'data': serializer.data}, status=201)


class TaskViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """ 
        Function to get all active task of user
        """
        user = userReg.objects.get(id=request.user.id)
        queryset = Task.objects.filter(user=user, is_active=True).order_by('created_at')

        filterset = TaskFilter(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response({"status": "failed", "errors": filterset.errors}, status=400)
        filtered_queryset = filterset.qs
        
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)

        serializer = TaskSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    def create(self, request):
        """
            Function to create Tasks
        """
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
                return Response({'status': 'failed', 'data': {'message': serializer.errors}}, status=422)
        serializer.save()
        return Response({"status": "success", "data": serializer.data}, status=201)

    def patch(self, request, pk=None):
        """
            Update Tasks
        """
        task_obj = Task.objects.filter(id=pk, user=request.user).first()
        if task_obj:
            serializer = TaskSerializer(task_obj, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 'failed', 'data': {"message": serializer.errors}}, 422)
            serializer.save()
            return Response({"message": "Task updated succesfully"}, 200)
        else:
            return Response({"message": f"Task with id {pk} not found"}, 400)
        
    def destroy(self, request, pk=None):
        """
            Delete or mark task as inactive
        """
        task_obj = Task.objects.filter(id=pk, user=request.user).first()
        if task_obj:
            task_obj.is_active = False
            task_obj.save()
        else:
            return Response({"message": f"Task with id {pk} and user {request.user} is not found"}, 400)
        return Response({"status": "success", "message": "Task deleted successfully"}, status=200)