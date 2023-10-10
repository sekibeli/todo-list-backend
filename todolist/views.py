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
        # Du könntest hier zusätzliche Logik hinzufügen, wenn du möchtest, z. B.:
        # request.data['author'] = request.user.id
        # Beachte jedoch, dass dies von deinem Datenmodell und deinen Anforderungen abhängt.

        return super(AddTodoView, self).create(request, *args, **kwargs)

    # def post(self, request):
    #     serializer = TodoItemSerializer(data=request.data)
   
    def perform_create(self, serializer):
        # Dies stellt sicher, dass der Autor des Todo-Items der aktuell eingeloggte Benutzer ist
        serializer.save(author=self.request.user)    
        
class SingleTodoItemView(APIView):  # Ein einzelner Todo wird angezeigt
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  #permissions.IsAdminUser
    
    # def get(self, request, format=None):
    #     todos =  TodoItem.objects.filter(author=request.user)
    #     serializer = TodoItemSerializer(todos, many=True)
    #     return Response(serializer.data)
    
    def get(self, request, todo_id=None, format=None):
        if todo_id:
             todo = get_object_or_404(TodoItem, id=todo_id, author=request.user)
             serializer = TodoItemSerializer(todo)
        else:
             todos = TodoItem.objects.filter(author=request.user)
             serializer = TodoItemSerializer(todos, many=True)

        return Response(serializer.data)
    

    