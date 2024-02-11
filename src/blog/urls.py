"""Defines url patterns for the blog app"""
from django.urls import path

from .views import NewBlogView, UpdateBlogView, NewBlogPostView, UpdateBlogPostView, BlogPostDetailsView, SharePostWithBlog, SharedBlogView, StopSharingPostwithBlog

app_name = 'blog'
urlpatterns = [
    path('new/', NewBlogView.as_view(), name='new-blog'),
    path('<int:pk>/update/', UpdateBlogView.as_view(), name='update-blog'),
    path('post/new/', NewBlogPostView.as_view(), name='new-blog-post'),
    path('post/<int:pk>/update', UpdateBlogPostView.as_view(), name='update-blog-post'),
    path('post/<int:pk>/', BlogPostDetailsView.as_view(), name='blog-post-details'),

    # Sharing functionality
    path('post/<int:pk>/share/', SharedBlogView.as_view(), name='share-blog-post-with-blog'),
    path('post/<int:post_pk>/share/to/<int:blog_pk>/', SharePostWithBlog.as_view(), name='share-post-with-blog'),
    path('post/<int:post_pk>/stop/share/to/<int:blog_pk>/', StopSharingPostwithBlog.as_view(), name='stop-sharing-post-with-blog'),
]