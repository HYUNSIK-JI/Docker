from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from users.models import User
from .serializers import ReviewSerializer, CommentSerializer, ReviewBestSerializer
from users.views import AuthAPIView
from .models import Articles, Comment
import jwt
from django.db.models import Q, Count
from drfproject.settings import SECRET_KEY, SIMPLE_JWT
# Create your views here.

class ReviewList(APIView):
    def get(self, request):
        reviews = Articles.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            access = request.COOKIES.get('access', None)
            
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            
            pk = payload.get('user_id')
            
            serializer.save(user=User.objects.get(pk=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetail(APIView):
    def get_object(self, pk):
        try:
            return Articles.objects.get(pk=pk)
        except Articles.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        review = self.get_object(pk)
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    def patch(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewCommentList(APIView):

    def get(self, request, pk):
        articles = Articles.objects.get(pk=pk)
        comments = Comment.objects.filter(ariticles_id=articles.pk).order_by("-pk")
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            access = request.COOKIES.get('access', None)
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            user_pk = payload.get('user_id')
            
            serializer.save(ariticles=Articles.objects.get(pk=pk), user=User.objects.get(pk=user_pk))
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewComment(APIView):

    def get_object(self, pk, comment_pk):
        try:
            return Comment.objects.get(id=comment_pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, requset, pk, comment_pk, format=None):
        comment = self.get_object(pk, comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, comment_pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, comment_pk, format=None):
        comment = self.get_object(pk, comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewBest(APIView):
    def get(self, request):
        reviews = Articles.objects.annotate(nums=Count('like_articles')).order_by("-nums")
        serializer = ReviewBestSerializer(reviews, many=True)
        return Response(serializer.data)

class Reviewlike(APIView):

    def get(self, request, pk):
        review = Articles.objects.get(pk=pk)
        access = request.COOKIES.get('access', None)
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
        user_pk = payload.get('user_id')

        user = User.objects.get(pk=user_pk)

        if user in review.like_articles.all():
            print(review.like_articles.all(), 1)
            review.like_articles.remove(user)
            print(review.like_articles.all(), 2)
        else:
            print(review.like_articles.all(), 3)
            review.like_articles.add(user)
            print(review.like_articles.all(), 4)
        print(review.like_articles.all())
        serializer = ReviewBestSerializer(user)
        return Response(serializer.data)