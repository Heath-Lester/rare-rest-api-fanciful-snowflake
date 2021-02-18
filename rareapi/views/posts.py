"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, Author, Category, User, PostTag


class Posts(ViewSet):

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        user = User.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.post_time = request.data["post_time"]
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.deleted = request.data["deleted"]

        author = Author.objects.get(pk=request.data["author_id"])
        post.author = author

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
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an post

        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.post_time = request.data["post_time"]
        post.image_url = request.data["image_url"]
        post.approved = request.data["approved"]
        post.deleted = request.data["deleted"]

        author = Author.objects.get(pk=request.data["author_id"])
        post.author = author

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
        user = User.objects.get(user=request.auth.user)
        posts = Post.objects.all()

        # Set the `joined` property on every post
        for post in posts:
            post.joined = None

            try:
                PostTag.objects.get(post=post, user=user)
                post.joined = True
            except PostTag.DoesNotExist:
                post.joined = False

        # Support filtering posts by tag
        tag = self.request.query_params.get('tag_id', None)
        if tag is not None:
            posts = posts.filter(tag__id=tag)

        serializer = postSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostUserSerializer(serializers.ModelSerializer):
    """JSON serializer for post creators's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for tag on post"""
    user = PostUserSerializer(many=False)

    class Meta:
        model = User
        fields = ['user']

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'author_id', 'tag')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    user = PostUserSerializer(many=False)
    tag = TagSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'post_time', 'image_url', 'approved', 'deleted', 'author_id', 'category_id')