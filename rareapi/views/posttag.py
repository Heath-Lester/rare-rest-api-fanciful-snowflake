# Author: Ted
# Purpose: Get some PostTags server-side

"""View module for handling requests about tags"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rareapi.models import PostTag, Tag, Post

class PostTags(ViewSet):

    def create(self, request):
        """Handle POST operations for postTags
        
            Returns:
        Response -- JSON serialized tag instance
        """

        postTag = PostTag()
        post = Post.objects.get(pk=request.data["postId"])
        tag = Tag.objects.get(pk=request.data["tagId"])

        postTag.post = post
        postTag.tag = tag

        try:
            postTag.save()
            serializer = PostTagSerializer(postTag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag

        Returns:
            Response -- JSON serialized tag instance
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a tag

        Returns:
            Response -- Empty body with 204 status code
        """
        tag = Tag()
        tag.label = request.data["label"]
        token = Token.objects.get(user = request.auth.user)
        tag.author_id = token

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single postTag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            postTag = PostTag.objects.get(pk=pk)
            postTag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        # Get the current authenticated user
        tags = Tag.objects.all()

        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'author_id', 'label')