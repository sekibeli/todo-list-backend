from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #permissions.IsAdminUser
    
    def get(self, request, format=None):
        todos =  TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class AddTodoView(generics.CreateAPIView):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # request.data['author'] = request.user.id
        return super(AddTodoView, self).create(request, *args, **kwargs)

   
    def perform_create(self, serializer):
        # Dies stellt sicher, dass der Autor des Todo-Items der aktuell eingeloggte Benutzer ist
        serializer.save(author=self.request.user)    
        
class SingleTodoItemView(APIView):  # Ein einzelner Todo wird angezeigt
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #permissions.IsAdminUser
       
    def get(self, request, todo_id=None, format=None):
        if todo_id:
             todo = get_object_or_404(TodoItem, id=todo_id, author=request.user)
             serializer = TodoItemSerializer(todo)
       
        return Response(serializer.data)
    
class DeleteTodoView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #permissions.IsAdminUser
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class UpdateName(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #permissions.IsAdminUser
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.title = request.data.get("title")
        instance.checked = request.data.get("checked")
        instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)