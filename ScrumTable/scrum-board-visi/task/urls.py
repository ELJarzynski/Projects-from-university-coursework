from django.urls import path
from .views import (CreateTask, RetrieveTaskListView, RetrieveSingleTaskView,
                    UpdateTaskView, DeleteTaskView, CreateTaskUser, RetrieveTaskUserList,
                    DeleteTaskUser, UpdateTaskSectionView)


app_name = 'task'

urlpatterns = [
    path('create/', CreateTask.as_view(), name='create-task'),
    path('<int:section_id>/task_list/', RetrieveTaskListView.as_view(), name='retrive-task-list'),
    path('retrive_task/<int:task_id>', RetrieveSingleTaskView.as_view(), name='retrive-task'),
    path('update_task/<int:task_id>', UpdateTaskView.as_view(), name='update-task'),
    path('update_task_section/<int:task_id>/section/<int:section_id>', UpdateTaskSectionView.as_view(), name='update-task-section'),
    path('delete_task/<int:task_id>', DeleteTaskView.as_view(), name='delete-task'),
    path('<int:board_id>/create_task_user/<int:task_id>', CreateTaskUser.as_view(), name='create-task-user'),
    path('<int:task_id>/task_user_list/', RetrieveTaskUserList.as_view(), name='retrive-task-user-list'),
    path('<int:task_id>/user/<int:user_id>/delete/', DeleteTaskUser.as_view(), name='delete_task_user'),
]