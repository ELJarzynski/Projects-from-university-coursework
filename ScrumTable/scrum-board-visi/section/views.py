from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from .models import Section
from .serializer import SectionSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from user.models import User
from board.models import Board

# Create your views here.


class CreateSectionView(generics.CreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        board_id = self.kwargs['board_id']
        name = self.request.data.get('name')

        board_instance = Board.objects.get(pk=board_id)

        serializer.save(name=name, board=board_instance)


class RetrieveSectionListView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('board_id')
        board_instance = Board.objects.get(pk=board_id)

        return Section.objects.filter(board=board_instance)


class UpdateSection(generics.UpdateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        board_id = self.kwargs['board_id']
        section_id = self.kwargs['pk']  # Retrieve section ID from URL

        # Retrieve the section object to be updated
        section = self.get_object()

        data = request.data.copy()
        data['board'] = board_id # podmianka

        # Update the section with the request data
        serializer = self.get_serializer(section, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class DeleteSectionView(generics.DestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        section_id = self.kwargs.get('section_id')

        section_to_delete = Section.objects.get(id=section_id)

        section_to_delete.delete()

        return Response({'message': 'section deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

