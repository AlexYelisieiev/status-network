from django.urls import path
from .views import (
    StatusCreateView,
    StatusEditView,
    StatusLikeView,
    StatusDetailView,
    generate_ai_summary_view,
)


urlpatterns = [
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('edit/by_status_id/<int:id>', StatusEditView.as_view(), name='status_edit_by_status_id'),
    path('edit/by_user_id/<int:user_id>', StatusEditView.as_view(), name='status_edit_by_user_id'),
    path('like/<int:status_id>', StatusLikeView.as_view(), name='status_like'),
    path('detail/<int:pk>', StatusDetailView.as_view(), name='status_detail'),
    path('generate/summary/<int:status_id>',
         generate_ai_summary_view, name='status_generate_ai_summary')
]
