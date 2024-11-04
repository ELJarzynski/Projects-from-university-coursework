from django.urls import path
from .views import CreateSectionView, RetrieveSectionListView, UpdateSection, DeleteSectionView

app_name = 'section'

urlpatterns = [
    path('<int:board_id>/create_section/', CreateSectionView.as_view(), name='create-section'),
    path('<int:board_id>/sections/', RetrieveSectionListView.as_view(), name='section-list'),
    path('<int:board_id>/update_section/<int:pk>/', UpdateSection.as_view(), name='update-section'),
    path('delete_section/<int:section_id>', DeleteSectionView.as_view(), name='delete-section'),
]