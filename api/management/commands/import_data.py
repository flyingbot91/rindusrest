import os
import logging

import requests

from django.core.management.base import BaseCommand

from api.models import Comment, Post

logger = logging.getLogger(__name__)

API_URL = "https://jsonplaceholder.typicode.com"
API_URL_COMMENTS = os.path.join(API_URL, "comments")
API_URL_POSTS = os.path.join(API_URL, "posts")

post_mapping = {
    "body": "body",
    "id": "id",
    #"user_id": "userId",
    "title": "title",
}
comment_mapping = {
    "body": "body",
    "email": "email",
    "name": "name",
    "post_id": "postId",
}

class Command(BaseCommand):
    help="Quick and dirty tool to import data from remote API"

    def fetch_data(self, url: str) -> list:
        """Fetch data from API endpoint.

        :param      url:        API url endpoint
        :type       url:        str
        :return     data:       Fetched endpoint data
        :rtype      data:       list
        """

        data = {}
        try:
            response = requests.get(url)
            data = response.json()
            logger.info(f"Fetched {len(data)} items from url '{url}'")
        except Exception as err:
            logger.error(f"Cannot fetch data from url '{url}'. Cause: {err}")
            raise

        return data

    def ingest_items(self, model, mapping: dict, items: list) -> None:
        """Ingest items in the DDBB.

        :param      model:      Django model
        :type       model:      django.db.model
        :param      mapping:    Django model field mapping
        :type       mapping:    dict
        :param      items:      List of objects of model <model>
        :type       items:      django.db.models.QuerySet
        """

        try:
            objs = model.objects.bulk_create(
                [
                    model(
                        **{key:item[value] for key,value in mapping.items()}
                    ) for item in items
                ]
            )
            logger.info(f"{len(objs)} objects of model {model} created.")
        except Exception as err:
            logger.error(f"Cannot ingest items for model {model}. Cause: {err}")
            raise

    def handle(self, *args, **options):
        """Main method."""
        logger.info("======================================")
        logger.info("=== Import data process started    ===")
        logger.info("======================================")

        try:
            posts = self.fetch_data(API_URL_POSTS)
            self.ingest_items(Post, post_mapping, posts)
            comments = self.fetch_data(API_URL_COMMENTS)
            self.ingest_items(Comment, comment_mapping, comments)
        except Exception:
            logger.error("Cannot import data from API")
        finally:
            logger.info("=== Import data process terminated ===")
