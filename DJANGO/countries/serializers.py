from rest_framework import serializers
from .models import Country, Comment1, Photo


class PhotoSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Photo
        fields = ['image']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    country_code = serializers.ReadOnlyField(source = 'Country.country_code')
    images = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Country
        fields = ("id", "title", "content", "created_at", "updated_at", "user", "country_code", "images")
    
    
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    countries = serializers.ReadOnlyField(source = "country.pk")
    comment_pk = serializers.ReadOnlyField(source = "comment.pk")

    class Meta:
        model = Comment1
        fields = ("id", "countries", "content", "created_at", "updated_at", "user", "comment_pk", "country_code")

class ReviewBestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.email')
    like = serializers.ReadOnlyField(source = "country.like_country")
    created_at = serializers.ReadOnlyField(source = "country.created_at")
    updated_at = serializers.ReadOnlyField(source = "country.updated_at")
    class Meta:
        model = Country
        fields = ("id", "title", "content", "created_at", "updated_at", "user", "like", "country_code")