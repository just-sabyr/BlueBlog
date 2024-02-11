from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, View

from blog.forms import BlogForm

from django.http.response import HttpResponseForbidden
from blog.models import Blog, BlogPost
from blog.forms import BlogPostForm

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class NewBlogView(CreateView):
    form_class = BlogForm
    template_name = 'blog/blog_settings.html'

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.owner = self.request.user
        blog_obj.slug = slugify(blog_obj.title)

        blog_obj.save()
        return HttpResponseRedirect(reverse('blueblogs:home'))
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if Blog.objects.filter(owner=user).exists():
            return HttpResponseForbidden("You can not create more than one blog per account.")
        else:
            return super(NewBlogView, self).dispatch(request, *args, **kwargs)
        
class UpdateBlogView(UpdateView):
    form_class = BlogForm
    template_name = 'blog/blog_settings.html'
    success_url = '/'
    model = Blog

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogView, self).dispatch(request, *args, **kwargs)
    
class NewBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = 'blog/blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewBlogPostView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        blog_post_obj = form.save(commit=False)
        blog_post_obj.blog = Blog.objects.get(owner=self.request.user)
        blog_post_obj.slug = slugify(blog_post_obj.title)
        blog_post_obj.is_published = True

        blog_post_obj.save()

        return HttpResponseRedirect(reverse('blueblogs:home'))
    
class UpdateBlogPostView(UpdateView):
    form_class = BlogPostForm
    template_name = 'blog/blog_post.html'
    success_url = '/'
    model = BlogPost

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdateBlogPostView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(UpdateBlogPostView, self).get_queryset()
        return queryset.filter(blog__owner=self.request.user)
    
class BlogPostDetailsView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_post_details.html'

class SharedBlogView(TemplateView):
    template_name = 'blog/share_blog_post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SharedBlogView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, pk, **kwargs: Any) -> dict[str, Any]:
        blog_post = BlogPost.objects.get(pk=pk)
        currently_shared_with = blog_post.shared_to.all()
        currently_shared_with_ids = map(lambda x: x.pk, currently_shared_with)
        exclude_from_can_share_with = [blog_post.blog.pk] + list(currently_shared_with_ids)

        can_be_shared_with = Blog.objects.exclude(pk__in=exclude_from_can_share_with)

        return {
            'post': blog_post,
            'is_shared_with': currently_shared_with,
            'can_be_shard_with': can_be_shared_with
        }
    
class SharePostWithBlog(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super(SharePostWithBlog, self).dispatch(request, *args, **kwargs)

    def get(self, request, post_pk, blog_pk):
        blog_post = BlogPost.objects.get(pk=post_pk)
        if blog_post.blog.owner != request.user:
            return HttpResponseForbidden('You can share only the post you created.')
        
        blog = Blog.objects.get(pk=blog_pk)
        blog_post.shared_to.add(blog)

        return HttpResponseRedirect('blueblogs:home')
    
class StopSharingPostwithBlog(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StopSharingPostwithBlog, self).dispatch(request, *args, **kwargs)

    def get(self, request, post_pk, blog_pk):
        blog_post = BlogPost.objects.get(pk=post_pk)
        if blog_post.blog.owner != request.user:
            return HttpResponseForbidden('You can only stop sharing posts that you created.')

        blog = Blog.objects.get(pk=blog_pk)
        blog_post.shared_to.remove(blog)

        return HttpResponseRedirect(reverse('blueblogs:home'))