from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from. import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<slug:pk_slug>', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('facebook/',TemplateView.as_view(template_name='blog/index.html'), name="facebook")
]