"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.http.response import HttpResponsePermanentRedirect
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

class Users(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = User.objects.get(auth_token=pk)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to user resource

        Returns:
            Response -- JSON serialized list of users
        """
        # Get the current authenticated user
        users = User.objects.all().order_by('username')

        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        try:
            user = User.objects.get(auth_token=pk)
        except User.DoesNotExist as ex:
            return Response({'message': "don't tell me such sweet lies"}, status=status.HTTP_404_NOT_FOUND)

        if(user.is_active):
            user.is_active = False
            user.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "User is already deactivated"}, status=status.HTTP_409_CONFLICT)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        try:
            user = User.objects.get(auth_token=pk)
        except User.DoesNotExist as ex:
            return Response({'message': "don't tell me such sweet lies"}, status=status.HTTP_404_NOT_FOUND)

        if(not user.is_active):
            user.is_active = True
            user.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "User is already activated"}, status=status.HTTP_409_CONFLICT)


    @action(detail=True, methods=['post'])
    def deadminUser(self, request, pk=None):
        try:
            user = User.objects.get(auth_token=pk)
        except User.DoesNotExist as ex:
            return Response({'message': "Why you gotta do me like that?"}, status=status.HTTP_404_NOT_FOUND)

        if(user.is_staff):
            # Check for last admin; use a variable that filters through the is_staff field for all users
            """
            Select is_staff
            From users as u
            Where is_staff = true
            """
            admin_list = User.objects.filter(is_staff = 1)
            # if users.length > 1; Needs to be more than one admin left
            if len(admin_list) > 1:
                user.is_staff = False
                user.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "Nope! Last admin."})
        else:
            return Response({'message': "User is already deadmin"}, status=status.HTTP_409_CONFLICT)
    
    @action(detail=True, methods=['post'])
    def adminUser(self, request, pk=None):
        try:
            user = User.objects.get(auth_token=pk)
        except User.DoesNotExist as ex:
            return Response({'message': "Why you gotta do me like that?"}, status=status.HTTP_404_NOT_FOUND)

        if(not user.is_staff):
            user.is_staff = True
            user.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': "User is already admin"}, status=status.HTTP_409_CONFLICT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('is_staff', 'first_name', 'last_name', 'username', 'auth_token', 'is_active')