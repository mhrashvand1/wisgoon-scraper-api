from rest_framework.generics import GenericAPIView
from core.filters import PostFilter
from rest_framework.response import Response
from core.models import Post, Page
from core.serializers import PageSerializer, PostSerializer
from rest_framework.permissions import AllowAny
from datetime import datetime
from django.urls import reverse
from common.utils import get_abs_url
from core.tasks import run_crawler_task
from config.celery import app


class PageAPIView(GenericAPIView):
    """
    Insert the Wisgoon page username and view the posts. 
    ## Note that the page must be public, otherwise the posts cannot be crawled.
    """
    serializer_class = PageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)    
        username = request.data.get('username')
        response_msg = dict()

        # Check if a task is running with sent username
        if self.is_task_running("core.tasks.run_crawler_task", username):
            response_msg['detail'] = 'A worker is already crawling this page;The results can be viewed at the URL below.'
            response_msg['url'] = self.get_posts_url(username)
            return Response(response_msg, 200)
        
        # Check if there is a page with the specified username.
        qs = Page.objects.filter(username=username)
        if qs.exists():
            last_post_datetime = None
            newest_post = Post.objects.filter(page__username=username).order_by("-source_created").first()
            if newest_post:
                last_post_datetime = datetime.strftime(
                    newest_post.source_created,
                    "%Y-%m-%dT%H:%M:%S"
                )
            run_crawler_task.apply_async(kwargs={"username":username, "from_datetime":last_post_datetime})
        else:
            serializer.save()   
            run_crawler_task.apply_async(kwargs={"username":username, "from_datetime":None})
            
        response_msg['detail'] = 'The page is being crawled in the background and the results can be viewed at the URL below.'
        response_msg['url'] = self.get_posts_url(username)
        return Response(response_msg, 200)
    
    
    def is_task_running(self, task_name, username):
        i = app.control.inspect()
        active_tasks = i.active() or {}
        
        for worker_tasks in active_tasks.values():
            for task in worker_tasks:
                if task["name"] == task_name and task["kwargs"]["username"] == username:
                    return True

        return False
    
    def get_posts_url(self, username):
        url = reverse('core:post-list', kwargs={"username":username})
        return get_abs_url(url)
    
    
    
class PostListAPIView(GenericAPIView):
    
    serializer_class = PostSerializer
    permission_classes = [AllowAny,]
    filterset_class = PostFilter
    search_fields = ["title", "text",]
    ordering_fields = ["source_created",]
    
    def get_queryset(self):
        page_username = self.kwargs.get("username", '')
        return Post.objects.filter(page__username=page_username)
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class PostRetrieveAPIView(GenericAPIView):
    serializer_class = PostSerializer
    lookup_field = 'source_id'
    permission_classes = [AllowAny,]

    def get_queryset(self):
        page_username = self.kwargs.get("username", '')
        return Post.objects.filter(page__username=page_username)
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
