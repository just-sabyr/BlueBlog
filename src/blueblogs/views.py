from typing import Any
from django.shortcuts import render

from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from blog.views import Blog, BlogPost

class HomeView(TemplateView):
    template_name = 'blueblogs/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super(HomeView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if Blog.objects.filter(owner=self.request.user).exists():
                ctx['has_blog'] = True
                blog = Blog.objects.get(owner=self.request.user)

                ctx['blog'] = blog
                ctx['blog_posts'] = BlogPost.objects.filter(blog=blog)
                ctx['shared_posts'] = blog.shared_posts.all()

        return ctx
    
    