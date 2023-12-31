"""
URL configuration for todobackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.db import router
from django.urls import path
from todolist.views import AddTodoView, LoginView, TodoItemView, SingleTodoItemView, DeleteTodoView,UpdateTodoView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('todos/', TodoItemView.as_view(), name='todoItemView'),
    path('todo/<int:todo_id>/', SingleTodoItemView.as_view(), name='singleTodoItemView'),
    path('todo/addTodo/', AddTodoView.as_view(), name='addTodoView'),
    path('todo/delete/<int:pk>/', DeleteTodoView.as_view(), name='deleteTodoView' ),
    path('todo/update/<int:pk>/', UpdateTodoView.as_view(), name='updateTodoView'),

]
