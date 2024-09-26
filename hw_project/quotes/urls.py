from django.urls import path

from . import views
from .apps import QuotesConfig

app_name = QuotesConfig.name

urlpatterns = [
    path('', views.main, {"page_id": 1}, name='main'),
    path('add-author/', views.add_author, name='add-author'),
    path('add-quote/', views.add_quote, name='add-quote'),
    path('add-tag/', views.add_tag, name='add-tag'),
    path('author/<str:author_full_name_url>/', views.author, name='author'),
    path('tag/<str:tag_title>/', views.tag, {"page_id": 1}, name='tag'),
    path('top-tags/', views.top_tags, name='top-tags'),
    path('page/<int:page_id>/', views.main, name='main-page-id'),
    path('tag/<str:tag_title>/page/<int:page_id>/', views.tag, name='tag-page-id'),
]
