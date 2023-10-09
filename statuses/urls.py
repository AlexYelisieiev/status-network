from django.urls import path
from .views import StatusCreateView, StatusEditView

urlpatterns = [
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('edit/by_status_id/<id>', StatusEditView.as_view(), name='status_edit_by_status_id'),
    path('edit/by_user_id/<user_id>', StatusEditView.as_view(), name='status_edit_by_user_id'),
]
