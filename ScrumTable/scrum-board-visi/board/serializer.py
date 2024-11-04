from rest_framework import serializers
from user.serializer import UserSerializer
from . import models
from user.models import User


class BoardSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(read_only=True, format='%d %B %Y')
    due_date = serializers.DateField(format='%d %B %Y')

    class Meta:
        model = models.Board
        fields = (
            'id',
            'name',
            'description',
            'create_date',
            'due_date',
        )


class BoardUserSerializer(serializers.ModelSerializer):
    board = BoardSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              write_only=True)  # Only accept user ID during write operations
    user_detail = UserSerializer(source='user', read_only=True)
    is_owner = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.BoardUser
        fields = (
            'board',
            'user',
            'user_detail',
            'is_owner',
        )
