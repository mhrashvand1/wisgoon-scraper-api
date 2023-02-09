from rest_framework import serializers
from core.models import Page, Post
import requests
from rest_framework.exceptions import NotFound, ValidationError
from django.urls import reverse
from common.utils import get_abs_url


class PageSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True,)
     
    def validate_username(self, username):
        page_url = f"https://wisgoon.com/{username}"
        res = requests.get(page_url)
        if res.status_code == 200:
            return username
        elif res.status_code == 404:
            raise NotFound(f'Page with username {username} not found.')
        else:
            raise ValidationError(f'Error in getting page information with username: {username}')
    
    def create(self, validated_data):
        return Page.objects.create(**validated_data)
    
        
class PostSerializer(serializers.ModelSerializer):
    
    main_media = serializers.SerializerMethodField()
    other_media = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            "id", "source_id", "title", 
            "text", "main_media", "other_media",
            "source_created", "url", "detail"
        )
        
    def get_main_media(self, obj):
        try:
            main_media = obj.media_set.filter(is_main=True).first()
            return str(main_media.url)
        except:
            return
        
    def get_other_media(self, obj):
        try:
            other_media = obj.media_set.filter(is_main=False)
            result = [str(i.url) for i in other_media]
            return result
        except:
            return  
        
    def get_url(self, obj):
        return f"https://wisgoon.com/pin/{obj.source_id}/"
    
    def get_detail(self, obj):
        path = reverse("core:post-detail", kwargs={"username":obj.page.username, "source_id":obj.source_id})
        return get_abs_url(path)
