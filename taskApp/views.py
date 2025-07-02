from django.shortcuts import render

from rest_framework import viewsets, permissions, filters, status
from .models import Task
from .serializers import TaskSerializer, LoginSerializers, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .pagination import TaskPagination
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MarkTaskCompletedView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, owner=request.user)
        except Task.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        task.completed = True
        task.save()
        return Response(TaskSerializer(task).data)
    
class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializers)
    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = auth.authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserView(APIView):

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

