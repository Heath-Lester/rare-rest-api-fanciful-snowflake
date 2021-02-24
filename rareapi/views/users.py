"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import NullBooleanField
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Subscription
from rest_framework.authtoken.models import Token
from datetime import datetime

class Users(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user instance
        """
        try:
            user = User.objects.get(pk=pk)
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

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        if request.method == "POST":

            follower = Token.objects.get(user = request.auth.user)

            author = Token.objects.get(user = pk)

            try:
                subscription = Subscription.objects.get(follower=follower, author=author)
                return Response({'message': 'User already subscribes to this author.'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Subscription.DoesNotExist:
                subscription = Subscription()
                subscription.follower = follower
                subscription.author = author
                subscription.created_on = datetime.now()
                subscription.ended_on = NullBooleanField
                subscription.save()

                return Response({}, status=status.HTTP_201_CREATED)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('id', 'is_staff', 'first_name', 'last_name', 'username')