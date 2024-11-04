from rest_framework import serializers
from user.serializer import UserSerializer
from . import models
from user.models import User

class TaskSerializer(serializers.ModelSerializer):
    create_date = serializers.DateField(read_only=True, format='%d %B %Y')
    due_date = serializers.DateField(format='%d %B %Y')

    class Meta:
        model = models.Task
        fields = (
            'id',
            'name',
            'description',
            'section',
            'create_date',
            'due_date',
        )


class TaskUserSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              write_only=True)  # Only accept user ID during write operations
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = models.TaskUser
        fields = (
            'id',
            'task',
            'user',
            'user_detail',
        )