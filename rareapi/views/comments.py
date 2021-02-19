from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rareapi.models import Comment

class Comments(ViewSet):

	def list(self, request):

		comments = Comment.objects.all()

		serializer = CommentSerializer(comments, many=True, context={'request', request})

		return Response(serializer.data)
	
	def retrieve(self, request, pk=None):

		try:
			comment = Comment.objects.get(pk=pk)
			serializer = CommentSerializer(comment, context={'request', request})
			return Response(serializer.data)
		except Exception as ex:
			return HttpResponseServerError(ex)


	def create(self, request):

		user = Token.objects.get(user=request.auth.user)

		comment = Comment()
		comment.author = user
		comment.subject = request['subject']
		comment.comment = request['comment']
		comment.deleted = False

		try:
			comment.save()
			serializer = CommentSerializer(comment, context={'request', request})
			Response(serializer.data)
		except ValidationError as ex:
			return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):

		user = Token.objects.get(user=request.auth.user)

		comment = Comment.objects.get(pk=pk)
		comment.author = user
		comment.subject = request['subject']
		comment.comment = request['comment']
		comment.deleted = request['deleted']

		try:
			comment.save()
			serializer = CommentSerializer(comment, context={'request', request})
			Response(serializer.data)
		except ValidationError as ex:
			return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['author_id', 'subject', 'comment', 'deleted']