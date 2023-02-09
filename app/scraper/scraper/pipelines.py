import os
import sys
from itemadapter import ItemAdapter
from datetime import datetime
from asgiref.sync import sync_to_async

sys.path.append(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        '..', '..', 'api'
    )
)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
django.setup()

from django.db import transaction
from core.models import Post, Media, Page


class DBPipeline:
    
    async def process_item(self, item, spider):
        item = ItemAdapter(item).asdict()  
        try:
            await sync_to_async(self.insert_data)(item)  
        except:
            print(f"\n\n Ohh an error occurred while saving post: {item.get('source_id')}\n\n")
        return item


    def insert_data(self, item):
        with transaction.atomic():
            page = Page.objects.get(username=item.get('username'))
            source_created = datetime.strptime(
                item.get("source_created"),
                "%Y-%m-%d %H:%M:%S"
            )
            post, created = Post.objects.get_or_create(
                page=page, 
                source_id=item.get('source_id'),
                title=item.get('title'),
                text=item.get('text'),
                source_created=source_created
            )
            if created:
                # Create main media
                main_media_url = item.get("media").get("main_media")
                Media.objects.create(post=post, url=main_media_url, is_main=True)
                # Create other media
                other_media_urls = item.get("media").get("other_media")
                data = [Media(post=post, url=url) for url in other_media_urls]
                Media.objects.bulk_create(data)
                
            print(f"\n Post {item.get('source_id')} created successfullt. \n")
        