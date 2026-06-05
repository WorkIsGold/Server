from rest_framework import serializers
from django.contrib.auth.models import User
from .models import News


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=f"{validated_data['first_name']} {validated_data['last_name']}",
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class NewsSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = ['id', 'title', 'summary', 'content', 'author', 'author_name', 'date_created']
        read_only_fields = ['author', 'date_created']

    def validate_content(self, value):
        if len(value) < 50:
            raise serializers.ValidationError("Минимум 50 символов.")
        return value

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Заголовок должен содержать минимум 3 символа")
        return value