from django.urls import path
from .views import StatusCreateView, StatusEditView

urlpatterns = [
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('edit/<int:pk>/', StatusEditView.as_view(), name='status_edit')
]
