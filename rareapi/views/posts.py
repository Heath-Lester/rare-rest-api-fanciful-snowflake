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
from rest_framework.response import Response
from rareapi.models import Post, Category, Tag, PostTag

class Posts(ViewSet):
    
    # Likely becomes the most complicated function in the app
    # Has to include categories, tags  
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
            post.tags = matchingtags
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

        serializer = PostListSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def modifyTags(self, request, pk=None):
        """Managing tags posting onto posts"""

        # A user wants add a tag to a post
        if request.method == "POST":
            # The pk would be `2` if the URL above was requested
            post = Post.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            tag = Tag.objects.get(user=request.auth.user)

            try:
                # Determine if the tag is already signed up
                appending = PostTag.objects.get(
                    post=post, tag=tag)
                return Response(
                    {'message': 'Tag already up in this post.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except PostTag.DoesNotExist:
                # The user is not signed up.
                appending = PostTag()
                appending.post = post
                appending.tag = tag
                appending.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    
    Incorporates tags into a single unique post in Post Detail.
    """
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'publication_date', 'image_url', 'approved', 'deleted', 'author', 'category', 'tags')
        depth = 2

class PostListSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'publication_date', 'image_url', 'approved', 'deleted', 'author', 'category')
        depth = 2
