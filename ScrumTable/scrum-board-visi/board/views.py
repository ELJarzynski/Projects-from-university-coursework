from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Board, BoardUser
from .serializer import BoardSerializer, BoardUserSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from user.models import User

# Create your views here.


class CreateBoardView(generics.CreateAPIView):
    # Create Board
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # create board
        board = serializer.save()

        # create BoardUser with owner set to True
        user = self.request.user
        board_user = BoardUser.objects.create(
            board=board,
            user=user,
            is_owner=True
        )

        data = {
            'board': BoardSerializer(board).data,
            'board_user': BoardUserSerializer(board_user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

class RetrieveBoardView(generics.ListAPIView):
    # Get list of Boards that are bound to request user
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id

        # get all Boards that are bound to user
        queryset = Board.objects.filter(boarduser__user_id=user_id)

        return queryset

class RetrieveSingleBoardView(generics.RetrieveAPIView):
    # get details of single Board based on id in url
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        board_id = self.kwargs['board_id']  # Assuming you're passing the board_id in the URL

        # Retrieve the board if it exists and is bound to the user
        try:
            board = Board.objects.get(id=board_id, boarduser__user_id=user_id)
        except Board.DoesNotExist:
            raise NotFound("Board not found")

        return board


class CreateBoardUserView(generics.CreateAPIView):
    # Create BoardUser to given id of a board from url
    queryset = BoardUser.objects.all()
    serializer_class = BoardUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        board_id = self.kwargs.get('board_id')
        user = self.request.user
        # user_id = self.request.data.get('user')

        board_instance = Board.objects.get(pk=board_id)

        # Check for user existence and handle User.DoesNotExist within the serializer
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.validated_data['user']

        # Check if the user is the owner of the board
        board_user = BoardUser.objects.filter(board=board_instance, user=user).first()
        if not board_user or not board_user.is_owner:
            raise PermissionDenied({'message': 'You are not the owner of this board.'})

        # Check if the user is already assigned to this board
        if BoardUser.objects.filter(board=board_instance, user=user_instance).exists():
            raise ValidationError({'message': 'User is already assigned to this board.'})

        # No exceptions raised: save the instance
        serializer.save(board=board_instance, user=user_instance)


class ListBoardUsersView(generics.ListAPIView):
    # list of BoardUsers of given board id from url
    serializer_class = BoardUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        return BoardUser.objects.filter(board=board_id)


# POST id of user to delete or GET?
class DeleteBoardUserView(generics.DestroyAPIView):
    # delete BoardUser from board id given from url
    queryset = BoardUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board_id = self.kwargs.get('board_id')
        user_id = self.kwargs.get('user_id')

        # Check if the authenticated user is the owner of the board
        board_user = BoardUser.objects.filter(board=board_id, user=request.user, is_owner=True).first()
        if not board_user:
            raise PermissionDenied("You are not the owner of this board.")

        # Retrieve the board user instance to delete
        try:
            board_user_to_delete = BoardUser.objects.get(board=board_id, user=user_id)
        except BoardUser.DoesNotExist:
            return Response({'message': 'Board user not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Perform the deletion
        board_user_to_delete.delete()

        return Response({'message': 'Board user deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class DeleteBoardView(generics.DestroyAPIView):
    # Delete Board on given id from url
    queryset = Board.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        board_id = self.kwargs.get('board_id')

        # Check if the authenticated user is the owner of the board
        board_user = BoardUser.objects.filter(board=board_id, user=request.user, is_owner=True).first()
        if not board_user:
            raise PermissionDenied("You are not the owner of this board.")

        # Retrieve the board instance to delete
        try:
            board_to_delete = Board.objects.get(id=board_id)
        except BoardUser.DoesNotExist:
            return Response({'message': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the board
        board_to_delete.delete()

        return Response({'message': 'Board deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class UpdateBoardView(generics.UpdateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        board_id = self.kwargs.get('board_id')

        # Retrieve the board instance to edit
        try:
            board_to_edit = Board.objects.get(id=board_id)
        except BoardUser.DoesNotExist:
            return Response({'message': 'Board not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the owner of the board
        board_user = BoardUser.objects.filter(board=board_id, user=request.user, is_owner=True).first()
        if not board_user:
            raise PermissionDenied("You are not the owner of this board.")

        # Serialize the updated data
        serializer = self.get_serializer(board_to_edit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)