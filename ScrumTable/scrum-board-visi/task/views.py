from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Task, TaskUser
from .serializer import TaskSerializer, TaskUserSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from user.models import User
from section.models import Section
from board.models import Board
from board.models import BoardUser


class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Extract the section ID from the request data
        section_id = self.request.data.get('section')

        # Retrieve the section instance from the database
        try:
            section_instance = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            raise ValidationError({'message': 'section not found'})

        # Set the section instance for the task
        serializer.save(section=section_instance)


class RetrieveTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs['section_id']
        section_instance = Section.objects.get(id=section_id)

        queryset = Task.objects.filter(section=section_instance)

        return queryset


class RetrieveSingleTaskView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task_id = self.kwargs['task_id']

        task = Task.objects.get(id=task_id)

        return task


class UpdateTaskView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_id')

        task_to_edit = Task.objects.get(id=task_id)

        serializer = self.get_serializer(task_to_edit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UpdateTaskSectionView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        section_id = kwargs.get('section_id')

        try:
            task_to_edit = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"message": "Task does not exist."}, status=404)

        task_to_edit.section_id = section_id
        task_to_edit.save()

        serializer = self.get_serializer(task_to_edit)
        return Response(serializer.data)


class DeleteTaskView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        task_id = self.kwargs.get('task_id')

        task_to_delete = Task.objects.get(id=task_id)

        task_to_delete.delete()

        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CreateTaskUser(generics.CreateAPIView):
    queryset = TaskUser.objects.all()
    serializer_class = TaskUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        board_id = self.kwargs['board_id']

        user_id = self.request.data.get('user')
        task_id = self.kwargs['task_id']

        task_instance = Task.objects.get(pk=task_id)
        user_instance = User.objects.get(pk=user_id)

        try:
            board_instance = Board.objects.get(pk=board_id)  # check if board exists
        except Board.DoesNotExist:
            raise NotFound("Board does not exist")

        try:
            boarduser_instance = BoardUser.objects.get(board=board_instance, user=user_instance)  # check if user is assigned to board
        except BoardUser.DoesNotExist:
            raise NotFound("User is not assigned to given board")

        if TaskUser.objects.filter(task=task_instance, user=user_instance).exists():  # check if not duplicate
            raise ValidationError({'message': 'User is already assigned to this task.'})

        serializer.save(task=task_instance, user=user_instance)


class RetrieveTaskUserList(generics.ListAPIView):
    serializer_class = TaskUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        task_instance = Task.objects.get(id=task_id)

        queryset = TaskUser.objects.filter(task=task_instance)

        return queryset


class DeleteTaskUser(generics.DestroyAPIView):
    queryset = TaskUser.objects.all()
    serializer_class = TaskUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # Get the task ID and user ID from URL kwargs
        task_id = self.kwargs.get('task_id')
        user_id = self.kwargs.get('user_id')
        task_instance = Task.objects.get(id=task_id)
        user_instance = User.objects.get(id=user_id)

        # Retrieve the TaskUser instance
        try:
            task_user_instance = TaskUser.objects.get(task=task_instance, user=user_instance)
        except TaskUser.DoesNotExist:
            # Handle the case where TaskUser instance does not exist
            return Response({'message': 'TaskUser instance not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the TaskUser instance
        task_user_instance.delete()

        # Return a success response
        return Response({'message': 'TaskUser instance deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
