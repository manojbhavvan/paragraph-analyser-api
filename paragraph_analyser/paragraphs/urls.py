# paragraphs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path(
        "paragraphs/",
        views.ParagraphCreateAPIView.as_view(),
        name="paragraph-create",
    ),
    path("search/", views.SearchParagraphsAPIView.as_view(), name="search-paragraphs"),
]
