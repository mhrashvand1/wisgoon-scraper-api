from django.db import models
from common.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Page(BaseModel):
    username = models.CharField(
        max_length=300, 
        unique=True, 
        db_index=True, 
        blank=False, 
        null=False,
        verbose_name=_('username')
    )
    
    class Meta:
        db_table = 'Page'
        verbose_name = _('page')
        verbose_name_plural = _('pages')     
  
        
class Post(BaseModel):
    page = models.ForeignKey(
        to='core.Page', to_field='username',
        on_delete=models.CASCADE, related_name='posts',
        verbose_name=_('page')
    )
    source_id = models.PositiveBigIntegerField(
        unique=True, db_index=True,
        blank=False, null=False, verbose_name=_('source_id')
    )
    title = models.TextField(blank=True, null=False, verbose_name=_('title'))
    text = models.TextField(blank=True, null=False, verbose_name=_('text'))
    source_created = models.DateTimeField(blank=False, null=False, verbose_name=_('source_created'))
    
    class Meta:
        db_table = 'Post'
        verbose_name = _('post')
        verbose_name_plural = _('posts') 
        ordering = ['-source_created', ]
        
        
class Media(BaseModel):
    post = models.ForeignKey(
        to='core.Post', to_field='source_id',
        on_delete=models.CASCADE, related_name='media_set',
        verbose_name=_('post')   
    )
    url = models.URLField(blank=False, null=False, verbose_name=_('url'))
    is_main = models.BooleanField(default=False, verbose_name=_('is_main'))
    
    class Meta:
        db_table = 'Media'
        verbose_name = _('media')
        verbose_name_plural = _('media') 
    