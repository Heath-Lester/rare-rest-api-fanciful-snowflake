"""View module for handling requests about events"""
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rareapi.models import Post, Category, Tag

class Posts(ViewSet):

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """

        post = Post()
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.publication_date = datetime.now()
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.deleted = request.data["deleted"]
        token = Token.objects.get(user = request.auth.user)
        post.author_id = token

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            post = Post.objects.get(pk=pk)
            """ 
            Select * 
            From Tag t
            Join PostTags pt
            On t.id = pt.tag_id
            Join Post p
            On p.id = pt.post_id
            Where p.id = ?
            """
            matchingtags = Tag.objects.filter(tagging__post=post)
            print(matchingtags.query)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.publication_date = datetime.now()
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.deleted = request.data["deleted"]
        token = Token.objects.get(user = request.auth.user)
        post.author_id = token

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        # Get the current authenticated user
        posts = Post.objects.all()

        # Support filtering posts by tag
        # tag = self.request.query_params.get('tag_id', None)
        # if tag is not None:
        #     posts = posts.filter(tag__id=tag)

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'publication_date', 'image_url', 'approved', 'deleted', 'author', 'category', 'label')
        depth = 2
