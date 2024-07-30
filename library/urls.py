from . import views
from django.urls import path

urlpatterns = [
    path('', views.library_view, name='library'),
    path('edit/<int:pk>', views.piece_edit, name='piece_edit'),
    path('delete/<int:pk>', views.piece_delete, name='piece_delete'),
]