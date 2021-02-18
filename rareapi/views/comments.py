from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment

class Comments(ViewSet):

	def list(self, request):

		comments = Comment.objects.all()

		serializer = CommentSerializer(comments, many=True, context={'request', request})

		return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['author_id', 'subject', 'comment', 'deleted']