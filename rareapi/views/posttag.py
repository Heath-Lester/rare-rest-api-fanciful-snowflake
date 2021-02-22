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
        post = Post.objects.get(pk=request.data["post_id"])
        tag = Tag.objects.get(pk=request.data["tag_id"])

        postTag.post = post
        postTag.tag = tag

        try:
            postTag.save()
            serializer = PostTagSerializer(postTag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #     """Handle GET requests for single tag

    #     Returns:
    #         Response -- JSON serialized tag instance
    #     """
    #     try:
    #         postTag = PostTag.objects.get(pk=pk)
    #         serializer = PostTagSerializer(postTag, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single postTag

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            postTag = PostTag.objects.get(pk=pk)
            postTag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PostTag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to tags resource

        Returns:
            Response -- JSON serialized list of tags
        """
        postTags = PostTag.objects.all()

        # Filter postTags by post.
        post = self.request.query_params.get("post_id", None)

        if post is not None:
            postTags = postTags.filter(post_id=post)

        serializer = PostTagSerializer(
            postTags, many=True, context={'request': request})
        return Response(serializer.data)

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')

class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""

    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id', 'tag')
        depth = 1