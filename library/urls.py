from . import views
from django.urls import path

urlpatterns = [
    #Library Page - CRUD for Pieces
    path('', views.library_view, name='library'), 
    path('piece/<int:pk>', views.piece_view, name='piece_view'),
    path('piece/<int:pk>/edit', views.piece_edit, name='piece_edit'),
    path('piece/<int:pk>/delete', views.piece_delete, name='piece_delete'),

    #Piece View Page - CRUD for Parts
    path('part/<int:pk>', views.part_view, name='part_view'),
    path('part/<int:pk>/pdf', views.part_pdf_view, name='part_pdf_view'),
    path('part/<int:pk>/edit', views.part_edit, name='part_edit'),
    path('part/<int:pk>/delete', views.part_delete, name='part_delete'),
]