from . import views
from django.urls import path

urlpatterns = [
    path('',views.setlist_list, name='setlist'),
    path('<int:pk>', views.setlist_view, name='setlist_view'),
    path('add/', views.setlist_add, name='setlist_add'),
    path('edit/<int:pk>', views.setlist_edit, name='setlist_edit'),
    path('delete/<int:pk>', views.setlist_delete, name='setlist_delete'),
]