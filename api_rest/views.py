from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  

from .models import User
from .serializers import userSerializer


import json

@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':
        users = User.objects.all()

        serializer = userSerializer(users, many=True)
        return Response(serializer.data)
    
    return Response({"message": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):

    try:
        user = User.objects.get(pk=nick)

    except: 
        Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = userSerializer(user)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = userSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD 

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manage(request):

    # ACESSANDO DADOS 

    if request.method == 'GET':

        try:
            if request.GET["user"]:

                user_nickname = request.GET["user"]


                try:
                    user = User.objects.get(pk=user_nickname)
                except:
                    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = userSerializer(user)
                return Response(serializer.data)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # CRIANDO DADOS
   
    if request.method == 'POST':
        new_user = request.data

        serializer = userSerializer(data=new_user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# EDITANDO DADOS

    if request.method == 'PUT':

        nickname = request.data["user_nickname"]

        try:
            updated_user = User.objects.get(pk=nickname)
        except:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        print(request.data)

        serializer = userSerializer(updated_user, data=request.data)

        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

# DELETANDO DADOS
    if request.method == 'DELETE':  
        try:
            user_to_delete = User.objects.get(pk=request.data["user_nickname"])
            user_to_delete.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)