from django.urls import path
from core.views import PageAPIView, PostListAPIView, PostRetrieveAPIView

app_name = 'core'
urlpatterns = [
    path('', PageAPIView.as_view(), name='page'),
    path('<str:username>/posts/', PostListAPIView.as_view(), name='post-list'),
    path('<str:username>/posts/<int:source_id>/', PostRetrieveAPIView.as_view(), name='post-detail'),
]
