from rest_framework import serializers
from .models import User, Address, Geo, Company, Post, Comment, Album, Photo, Todo

# Geo Serializer
class GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geo
        fields = ['lat', 'lng']

# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode', 'geo']

# Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']

    def create(self, validated_data):
        # Address ve Geo verilerini işleme
        address_data = validated_data.pop('address')
        geo_data = address_data.pop('geo')
        geo = Geo.objects.create(**geo_data)
        address = Address.objects.create(geo=geo, **address_data)

        # Company verisini işleme
        company_data = validated_data.pop('company')
        company = Company.objects.create(**company_data)

        # User verisini oluşturma
        user = User.objects.create(address=address, company=company, **validated_data)
        return user

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['userId', 'id', 'title', 'body']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.PrimaryKeyRelatedField(source="post", queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['postId', 'id', 'name', 'email', 'body']

# Album Serializer
class AlbumSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())

    class Meta:
        model = Album
        fields = ['userId', 'id', 'title']

# Photo Serializer
class PhotoSerializer(serializers.ModelSerializer):
    albumId = serializers.PrimaryKeyRelatedField(source="album", queryset=Album.objects.all())

    class Meta:
        model = Photo
        fields = ['albumId', 'id', 'title', 'url', 'thumbnail_url']


class TodoSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source="user", queryset=User.objects.all())

    class Meta:
        model = Todo
        fields = ['userId', 'id', 'title', 'completed']