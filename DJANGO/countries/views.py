from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from users.models import User
from .serializers import ReviewSerializer, CommentSerializer, ReviewBestSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from users.views import AuthAPIView
from .models import Country, Comment1, Photo
import jwt, io, json
from django.db.models import Q, Count
from drfproject.settings import SECRET_KEY, SIMPLE_JWT

# Create your views here.

class ReviewList(APIView):
    def get(self, request, country_code):
        reviews = Country.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request, country_code):
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            access = request.COOKIES.get('access', None)
            
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            
            pk = payload.get('user_id')
            
            serializer.save(user=User.objects.get(pk=pk), country_code=country_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get_object(self, pk, country_code):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404
    def get(self, request, pk, country_code):
        review = self.get_object(pk, country_code)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    def patch(self, request, pk, country_code):
        review = self.get_object(pk, country_code)
        serializer = ReviewSerializer(review, data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, country_code):
        review = self.get_object(pk, country_code)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class ReviewCommentList(APIView):

    def get(self, request, pk, country_code):
        country = Country.objects.get(pk=pk)
        comments = Comment1.objects.filter(country_id=country.pk).order_by("-pk")
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk, country_code):
        
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            access = request.COOKIES.get('access', None)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            user_pk = payload.get('user_id')
            
            serializer.save(ariticles=Country.objects.get(pk=pk), user=User.objects.get(pk=user_pk))
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewComment(APIView):

    def get_object(self, pk, comment_pk, country_code):
        try:
            return Comment1.objects.get(id=comment_pk)
        except Comment1.DoesNotExist:
            raise Http404

    def get(self, requset, pk, comment_pk, country_code, format=None):
        comment = self.get_object(pk, comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, pk, comment_pk, country_code, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, comment_pk, country_code, format=None):
        comment = self.get_object(pk, comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewBest(APIView):
    def get(self, request, country_code):
        reviews = Country.objects.annotate(nums=Count('like_country')).order_by("-nums").filter(country_code=country_code)
        serializer = ReviewBestSerializer(reviews, many=True)
        return Response(serializer.data)

class Reviewlike(APIView):

    def get(self, request, pk, country_code):
        review = Country.objects.get(pk=pk)
        access = request.COOKIES.get('access', None)
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        user_pk = payload.get('user_id')

        user = User.objects.get(pk=user_pk)

        if user in review.like_country.all():
            review.like_country.remove(user)
        else:
            review.like_country.add(user)
            
        serializer = ReviewBestSerializer(review)
        return Response(serializer.data)