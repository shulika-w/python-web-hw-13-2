from datetime import datetime
import os
import re

import django
from mongoengine import connect, Document, StringField, ListField, ReferenceField, CASCADE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
django.setup()

import quotes.models

client_mongo = connect(
    host=f"mongodb+srv://milvus:Milvus@milvus.hmkzt.mongodb.net/?retryWrites=true&w=majority&appName=Milvus", ssl=True
)

# client_mongo = connect(
#     host=f"mongodb://localhost:27017/", ssl=True
# )

class Author(Document):
    fullname = StringField(required=True, max_length=150)
    born_date = StringField(max_length=150)
    born_location = StringField(max_length=150)
    description = StringField(max_length=10000)
    meta = {"allow_inheritance": True, "collection": "authors"}


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    meta = {"allow_inheritance": True, "collection": "quotes"}


if __name__ == '__main__':
    authors_in_mongo = Author.objects.all()
    quotes_in_mongo = Quote.objects.all()

    for author_in_mongo in authors_in_mongo:
        author = quotes.models.Author()
        author.full_name = author_in_mongo.fullname
        author.born_date = datetime.strptime(author_in_mongo.born_date, "%B %d, %Y")
        author.born_location = re.sub("^in ", "", author_in_mongo.born_location, flags=re.IGNORECASE)
        author.description = author_in_mongo.description
        author.save()

    for quote_in_mongo in quotes_in_mongo:
        quote = quotes.models.Quote()
        quote.quote = quote_in_mongo.quote
        quote.author = quotes.models.Author.objects.filter(full_name=quote_in_mongo.author.fullname).first()
        quote.save()

        for tag_in_mongo in quote_in_mongo.tags:
            tag = quotes.models.Tag()
            tag.title = tag_in_mongo
            if not quote.tags.filter(title=tag_in_mongo):
                if not quotes.models.Tag.objects.filter(title=tag_in_mongo):
                    tag.save()
                tag = quotes.models.Tag.objects.filter(title=tag_in_mongo).first()
                quote.tags.add(tag)

    tag = quotes.models.Tag.objects.filter(title="simile").first()
    tag.title = "smile"
    tag.save()

    tags = quotes.models.Tag.objects.all()
    for tag in tags:
        tag.title = tag.title.replace("#", "")
        tag.save()
