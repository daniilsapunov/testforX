from rest_framework import serializers
from .models import Link, Collection
from django.contrib.auth.models import User


class LinkSerializer(serializers.ModelSerializer):
    collections = serializers.PrimaryKeyRelatedField(many=True, queryset=Collection.objects.all())

    class Meta:
        model = Link
        fields = ['id', 'title', 'description', 'url', 'image', 'link_type', 'created_at', 'updated_at', 'collections']
        read_only_fields = ['user', 'created_at', 'updated_at', 'title', 'description', 'image', 'link_type']

    def create(self, validated_data):
        collections_data = validated_data.pop('collections')  # Извлекаем данные коллекций
        link = Link.objects.create(**validated_data)  # Создаем объект Link без коллекций

        # Добавляем коллекции для ссылки
        link.collections.set(collections_data)  # Устанавливаем коллекции

        return link


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class EmptySerializer(serializers.Serializer):
    pass
