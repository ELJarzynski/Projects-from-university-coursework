from django.urls import path
from .views import (CreateBoardView, CreateBoardUserView, RetrieveBoardView,
                    RetrieveSingleBoardView, ListBoardUsersView, DeleteBoardUserView, DeleteBoardView,
                    UpdateBoardView)

app_name = 'board'

urlpatterns = [
    path('create_board/', CreateBoardView.as_view(), name='board-create'),
    path('add_user/', CreateBoardUserView().as_view(), name='board-user-create'),
    path('list_board/', RetrieveBoardView.as_view(), name='board-list'),
    path('<int:board_id>/', RetrieveSingleBoardView.as_view(), name='retrieve-board'),
    path('<int:board_id>/add_user/', CreateBoardUserView.as_view(), name='add-user-to-oard'),
    path('<int:board_id>/users/', ListBoardUsersView.as_view(), name='board-users-list'),
    path('<int:board_id>/delete_user/<int:user_id>', DeleteBoardUserView.as_view(), name='board-user-delete'),
    path('<int:board_id>/delete_board/', DeleteBoardView.as_view(), name='board-delete'),
    path('<int:board_id>/edit_board/', UpdateBoardView.as_view(), name='board-edit'),
]
