from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category

class Categories(ViewSet):

	def list(self, request):

		categories = Category.objects.all()

		serializer = CategorySerializer(categories, many=True, context={'request', request})

		return Response(serializer.data)

	def retrieve(self, request, pk=None):

		try:
			category = Category.objects.get(pk=pk)
			serializer = CategorySerializer(category, context={'request', request})
			return Response(serializer.data)
		except Exception as ex:
			return HttpResponseServerError(ex)

	def create(self, request):

		category = Category()
		category.category = request.data['category']
		category.deleted = False

		try:
			category.save()
			serializer = CategorySerializer(category, context={'request', request})
			return Response(serializer.data)
		except ValidationError as ex:
			return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):

		category = Category.objects.get(pk=pk)
		category.category = request.data['category']
		category.deleted = request.data['deleted']

		category.save()

		return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Category
		fields = ['category', 'deleted']